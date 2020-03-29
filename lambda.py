import json


def dispatcher_handler(event, context):
    print(f"event: {event}")
    print(f"type: {event.get('type')}")
    print(f"items: {event.get('items')}")
    return {
        "statusCode": 200,
        "body": json.dumps(event, indent=2),
    }


def worker_handler(event, context):
    print(f"event: {event}")
    print(f"type: {event.get('type')}")
    print(f"item: {event.get('item')}")
    return {
        "statusCode": 200,
        "body": json.dumps(event, indent=2),
    }
