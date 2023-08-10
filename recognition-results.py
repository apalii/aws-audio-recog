import json
from decimal import Decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


td = TypeDeserializer()


def unmarshall(dynamo_obj: dict) -> dict:
    """Convert a DynamoDB dict into a standard dict."""
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in dynamo_obj.items()}


def lambda_handler(event, context):
    # Get the query string parameters
    query_string_parameters = event.get('queryStringParameters')

    # Get the job_id
    job_id = query_string_parameters.get('job_id')

    if not job_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required argument: job_id'}),
        }

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Query the DynamoDB table for the data with the specified job_id
    response = dynamodb.get_item(
        TableName='recognition-results',
        Key={
            'job_id': {'S': job_id}
        }
    )

    # Check if the response was successful
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'error': 'Job not found'
            })
        }

    result = unmarshall(response['Item'])

    # Return the data from the DynamoDB table
    return {
        'statusCode': 200,
        'body': json.dumps(result, cls=DecimalEncoder)
    }
