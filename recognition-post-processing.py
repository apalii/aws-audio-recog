import json
import boto3

s3_client = boto3.client("s3")
dynamodb = boto3.resource('dynamodb')


def find_substring(string, substring):
    """Finds the substring in the string and returns the start and end index."""

    start_index = string.find(substring)
    if start_index == -1:
        return {
            "plain_text": string,
            "was_present": False,
            "start_word_index": None,
            "end_word_index": None
        }

    end_index = start_index + len(substring) - 1
    return {
        "plain_text": string,
        "was_present": True,
        "start_word_index": start_index,
        "end_word_index": end_index
    }


def lambda_handler(event, context):
    # Get the bucket name and file name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    job_id = key.split('.')[0]

    # Check file format
    if not key.endswith('txt'):
        return

    # Get the file from S3
    file_data = s3_client.get_object(Bucket=bucket, Key=key)
    json_data = file_data['Body'].read().decode('utf-8')
    data = json.loads(json_data)
    transcript = data['results']['transcripts'][0]['transcript']

    table = dynamodb.Table("recognition-jobs")
    sentences = table.get_item(Key={'job_id': job_id})['Item']['sentences']

    # Find matches
    find_results = [
        find_substring(transcript, sentence) for sentence in sentences
    ]
    # Save results
    table_results = dynamodb.Table("recognition-results")
    data = {
        "job_id": job_id,
        "audio_url": "the_audio_url",
        "sentences": find_results
    }
    table_results.put_item(Item=data)
