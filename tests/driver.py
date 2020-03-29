import json

import boto3

reviews_input = {
    "job_type": "reviews",
    "items": ["url_0", "url_1", "url_N",],
}

statuses_input = {
    "job_type": "statuses",
    "items": [
        {"biz_id": "biz_0", "review_id": "review_0"},
        {"biz_id": "biz_1", "review_id": "review_1"},
        {"biz_id": "biz_2", "review_id": "review_2"},
    ],
}


def invoke_lambda(lambda_name, event, dry_run=False):
    aws_lambda = boto3.client("lambda")
    invocation_type = "DryRun" if dry_run else "Event"
    payload = json.dumps(event)
    aws_lambda.invoke(
        FunctionName=lambda_name, InvocationType=invocation_type, Payload=payload,
    )


if __name__ == "__main__":
    invoke_lambda("yelp_dispatcher_lambda", reviews_input)
