import json
import boto3

sqs = boto3.client("sqs")


def lambda_handler(event, context):
    queue_url = sqs.get_queue_url(QueueName="recognition")["QueueUrl"]
    request_id = context.aws_request_id

    message_to_sqs = {
        "request_id": request_id,
        "audio_url": event["audio_url"],
        "sentences": event["sentences"]
    }

    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_to_sqs)
    )

    return {"body": {
        "request_id": request_id,
        "message": "Your request was accepted successfully"
    }
    }
