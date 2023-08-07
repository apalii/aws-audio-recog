import json
import boto3

s3 = boto3.client("s3")
dynamodb = boto3.resource('dynamodb')
transcribe_client = boto3.client('transcribe')


def lambda_handler(event, context):
    sqs_record = event['Records'][0]
    body = json.loads(sqs_record['body'])

    request_id = body["request_id"]
    s3_uri = body["audio_url"]
    sentences = body["sentences"]

    output_file_name = f"{request_id}.txt"

    # Start the transcription job
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=request_id,
        LanguageCode='en-US',
        Media={
            'MediaFileUri': s3_uri
        },
        OutputBucketName='apalii-recognition-results',
        OutputKey=output_file_name
    )

    table = dynamodb.Table("recognition-jobs")
    table.put_item(Item={
        'job_id': request_id,
        'sentences': sentences
    })

    return {
        'statusCode': 200,
        'body': response
    }
