import boto3
import json
import os

# Initialize the S3 client
s3 = boto3.client('s3')
apigatewaymanagementapi = boto3.client('apigatewaymanagementapi')


def lambda_handler(event, context):
    # Parse the target_id from the Lambda event
    print(json.dumps(event))
    body = json.loads(event['body'])
    target_id = event['requestContext']['connectionId']
    message = body.get('message')
    bucket_name = 'a1ses'

    # List objects in the specified S3 bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)

    # Iterate through the objects to find the one that matches the target_id
    for obj in objects.get('Contents', []):
        object_key = obj['Key']

        # Check if the object key contains the target_id
        if target_id in object_key:
            # Retrieve the JSON content from the matched object
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            json_content = json.loads(response['Body'].read().decode('utf-8'))

            # Extract the 'connection_id' from the JSON data
            t_id = json_content.get('target_id')

    if t_id:
        # Specify your S3 bucket name

        # Search for the connection_id based on the target_id

        con = search_connection_id_by_t_id(bucket_name, t_id)
        print(con)

        if con:
            # Send the message to the found connection
            cn_id = search_connection_id_by_t_id(bucket_name, t_id)
            send_message_to_client(cn_id, message)
            return {
                'statusCode': 200,
                'body': json.dumps({'cn_id': cn_id})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'Connection ID not found for Target ID {target_id}.'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing target_id in Lambda event.'})
        }


def search_connection_id_by_t_id(bucket_name, t_id):
    try:
        # List objects in the specified S3 bucket
        objects = s3.list_objects_v2(Bucket=bucket_name)

        # Iterate through the objects to find the one that matches the t_id
        for obj in objects.get('Contents', []):
            object_key = obj['Key']
            print(t_id)
            # Check if the object key contains the t_id
            if object_key.endswith(f'_{t_id}.json'):
                # Extract the connection_id from the object key
                cn_id = object_key.split('/')[-1].split('_')[0]
                return cn_id

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message processed successfully'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def send_message_to_client(cn_id, message):
    try:
        # Use the connection ID to send the message to the target client
        apigatewaymanagementapi.post_to_connection(
            ConnectionId=cn_id,
            Data=message
        )
        print(f"Message sent to Connection ID {cn_id}: {message}")

    except Exception as e:
        print(f"Error sending message to Connection ID {cn_id}: {str(e)}")
