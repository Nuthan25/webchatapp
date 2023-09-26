import boto3
import json


s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Parse the user ID from the input event
    print(json.dumps(event))

    connection_id = event['requestContext']['connectionId']
    user_id = event['queryStringParameters']['userid']
    target_id =event['queryStringParameters']['targid']

    # Store the user ID and connection ID in the S3 bucket
    bucket_name = 'a1ses'
    object_key = f'connections/{connection_id}_{user_id}.json'

    try:
        # Create a dictionary with user_id and connection_id
        data = {
            'user_id': user_id,
            'target_id': target_id,
            'connection_id': connection_id
        }

        # Store the dictionary as a JSON object in S3
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json.dumps(data)
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': 'User ID and Connection ID stored in S3 successfully!'
    }