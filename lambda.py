import json
from dataclasses import dataclass

from typing import Dict


@dataclass
class LambdaJob:
    items: Dict
    foo: str


def handler(event, context):
    body = event.get("body")
    print(f"body: {body}")
    return {
        "statusCode": 200,
        "body": json.dumps(event, indent=2),
    }


def dispatcher_handler(event, context):
    ...


def worker_handler(event, context):
    ...
