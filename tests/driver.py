import json

import boto3
import jsonpickle
from tests.inputs import DispatcherInput


def invoke_lambda(lambda_name, event, dry_run=False):
    aws_lambda = boto3.client("lambda")
    invocation_type = "DryRun" if dry_run else "Event"
    payload = json.dumps(event)
    aws_lambda.invoke(
        FunctionName=lambda_name, InvocationType=invocation_type, Payload=payload,
    )


if __name__ == "__main__":
    invoke_lambda("YelpDispatcherLambda", jsonpickle.encode(DispatcherInput.REVIEWS))
    # invoke_lambda("YelpDispatcherLambda", jsonpickle.encode(DispatcherInput.STATUSES))
