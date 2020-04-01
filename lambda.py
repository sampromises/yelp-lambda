import json
import os

import boto3
from yelp_fetcher.reviews import fetch_reviews
from yelp_fetcher.statuses import fetch_status
from yelp_lambda.classes import (
    DispatcherJob,
    JobType,
    ReviewsArgs,
    StatusesArgs,
    WorkerJob,
    WorkerResult,
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

    dispatcher_job = DispatcherJob(**event)
    job_type = dispatcher_job.get("job_type")
    args_list = dispatcher_job.get("args_list")
    print(f"job_type: {job_type}")
    print(f"args_list: {args_list}")

    for args in args_list:
        worker_job = WorkerJob(job_type=job_type, args=args)
        WorkerLambda.invoke(worker_job)


def worker_handler(event, context):
    print(f"event: {event}")

    worker_job = WorkerJob(**event)
    job_type = worker_job.get("job_type")
    args = worker_job.get("args")
    print(f"job_type: {job_type}")
    print(f"args: {args}")

    if job_type == JobType.REVIEWS.value:
        args = ReviewsArgs(**args)
        result = fetch_reviews(args.get("user_id"), args.get("url"))
    elif job_type == JobType.STATUSES.value:
        args = StatusesArgs(**args)
        result = fetch_status(
            args.get("user_id"), args.get("biz_id"), args.get("review_id")
        )
    else:
        raise NotImplementedError(f"Unsupported job_type: {job_type}")

    worker_result = WorkerResult(job_type=job_type, result=result)
    ResultsSQS.send_message(worker_result)
