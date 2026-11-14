import json, os
import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def handler(event, context):
    user = event["requestContext"]["authorizer"]["jwt"]["claims"].get("email", "unknown")
    items = table.scan(Limit=20).get("Items", [])
    items = sorted(items, key=lambda i: i["run_id"], reverse=True)
    print(json.dumps({"audit": "read_placements", "user": user}))  # app-level audit log
    return {"statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(items, default=str)}
