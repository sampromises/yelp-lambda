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


def dispatcher_handler(event, context):
    print(f"event: {event}")

    dispatcher_job = DispatcherJob(**event)
    job_type = dispatcher_job.get("job_type")
    args_list = dispatcher_job.get("args_list")
    print(f"job_type: {job_type}")
    print(f"args_list: {args_list}")

    aws_lambda = boto3.client("lambda")
    for args in args_list:
        worker_job = WorkerJob(job_type=job_type, args=args)
        payload = json.dumps(worker_job)
        print(f"Invoking worker lambda with payload: {payload}")
        aws_lambda.invoke(
            FunctionName="yelp_worker_lambda", InvocationType="Event", Payload=payload,
        )


def worker_handler(event, context):
    print(f"event: {event}")

    worker_job = WorkerJob(**event)
    job_type = worker_job.get("job_type")
    args = worker_job.get("args")
    print(f"job_type: {job_type}")
    print(f"args: {args}")

    sqs = boto3.resource("sqs")
    queue_name = os.environ.get("RESULTS_QUEUE_NAME", "YelpResultsQueue")
    queue = sqs.get_queue_by_name(QueueName=queue_name)

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
    print(f"Enqueuing to SQS: {worker_result}")
    _json = json.dumps(worker_result, default=str)
    queue.send_message(MessageBody=_json)
    return _json
