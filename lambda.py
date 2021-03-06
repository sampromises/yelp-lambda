import json
import os
import time
from typing import List

import boto3
import jsonpickle
from yelp_fetcher.reviews import Review, fetch_reviews
from yelp_fetcher.statuses import ReviewStatus, fetch_status
from yelp_lambda.common_types import JobType
from yelp_lambda.dispatcher_types import DispatcherRequest
from yelp_lambda.worker_types import (
    ReviewsWorkerRequest,
    ReviewsWorkerResult,
    StatusesWorkerRequest,
    StatusesWorkerResult,
    WorkerRequest,
)


class WorkerLambda:
    _client = None

    @staticmethod
    def client():
        if WorkerLambda._client is None:
            WorkerLambda._client = boto3.client("lambda")
        return WorkerLambda._client

    @staticmethod
    def invoke(event):
        lambda_name = os.environ.get("WORKER_LAMBDA_NAME")
        payload = json.dumps(event)
        print(f"Invoking {lambda_name} with payload: {payload}")
        WorkerLambda.client().invoke(
            FunctionName=lambda_name, InvocationType="Event", Payload=payload,
        )


class ResultsSQS:
    _queue = None

    @staticmethod
    def queue():
        if ResultsSQS._queue is None:
            ResultsSQS._queue = boto3.resource("sqs").get_queue_by_name(
                QueueName=os.environ.get("RESULTS_QUEUE_NAME")
            )
        return ResultsSQS._queue

    @staticmethod
    def send_message(message):
        _json = json.dumps(message, default=str)
        print(f"Enqueuing to SQS, MessageBody={_json}")
        ResultsSQS.queue().send_message(MessageBody=_json)


def dispatcher_handler(event, context):
    print(f"event: {event}")
    request: DispatcherRequest = jsonpickle.decode(event)

    def batch(iterable, batch_size=10):
        for i in range(0, len(iterable), batch_size):
            yield iterable[i : min(i + batch_size, len(iterable))]

    for worker_requests in batch(request.get_worker_requests()):
        for worker_request in worker_requests:
            print(f"Sending WorkerRequest: {worker_request}")
            WorkerLambda.invoke(jsonpickle.encode(worker_request))
        time.sleep(5)


def _handle_reviews(request: ReviewsWorkerRequest):
    reviews: List[Review] = fetch_reviews(request.user_id, request.url)

    worker_result = jsonpickle.encode(
        ReviewsWorkerResult(user_id=request.user_id, reviews=reviews,)
    )

    ResultsSQS.send_message(worker_result)


def _handle_statuses(request: StatusesWorkerRequest):
    status: ReviewStatus = fetch_status(request.user_id, request.biz_id, request.review_id)

    worker_result = jsonpickle.encode(
        StatusesWorkerResult(
            user_id=status["user_id"],
            biz_id=status["biz_id"],
            review_id=status["review_id"],
            status=status["status"],
        )
    )

    ResultsSQS.send_message(worker_result)


def worker_handler(event, context):
    print(f"event: {event}")
    request: WorkerRequest = jsonpickle.decode(event)
    if request.job_type == JobType.REVIEWS.value:
        _handle_reviews(request)
    elif request.job_type == JobType.STATUSES.value:
        _handle_statuses(request)
    else:
        raise NotImplementedError(f"Unsupported JobType: {request.job_type}")
