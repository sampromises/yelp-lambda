import json

import boto3
from yelp_fetcher.reviews import get_reviews
from yelp_fetcher.statuses import fetch_status


def dispatcher_handler(event, context):
    print(f"event: {event}")
    job_type, items = event.get("job_type"), event.get("items")
    print(f"job_type: {job_type}")
    print(f"items: {items}")

    aws_lambda = boto3.client("lambda")
    for item in items:
        payload = json.dumps({"job_type": job_type, "item": item,})
        print(f"Invoking worker lambda with payload: {payload}")
        aws_lambda.invoke(
            FunctionName="yelp_worker_lambda", InvocationType="Event", Payload=payload,
        )


def worker_handler(event, context):
    print(f"event: {event}")
    job_type, item = event.get("job_type"), event.get("item")
    print(f"job_type: {job_type}")
    print(f"item: {item}")

    if job_type == "reviews":
        url = item.get("url")
        reviews = get_reviews(url)
        print(reviews)
        return reviews
    elif job_type == "statuses":
        user_id = item.get("user_id")
        biz_id = item.get("biz_id")
        review_id = item.get("review_id")
        statuses = fetch_status(user_id, biz_id, review_id)
        print(statuses)
        return statuses
    else:
        raise NotImplementedError(f"Unsupported job_type: {job_type}")
