import json

import boto3


def dispatcher_handler(event, context):
    print(f"event: {event}")
    job_type, items = event.get("job_type"), event.get("items")
    print(f"job_type: {job_type}")
    print(f"items: {items}")

    aws_lambda = boto3.client("lambda")
    for item in items:
        payload = json.dumps({"job_type": job_type, "item": item,})
        print(f"Invoking dispatcher lambda with payload: {payload}")
        aws_lambda.invoke(
            FunctionName="yelp_worker_lambda", InvocationType="Event", Payload=payload,
        )


def worker_handler(event, context):
    print(f"event: {event}")
    print(f"job_type: {event.get('job_type')}")
    print(f"item: {event.get('item')}")
