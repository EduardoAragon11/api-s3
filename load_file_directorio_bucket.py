import json
import boto3
import base64
import os
from urllib.parse import unquote_plus
import logging

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket name from environment variables or hard code it
    bucket_name = 'eaa-new-bucket'
    
    # Extract the filename from the request
    try:
        # The body of the event contains the base64-encoded file data
        body = event['body']
        if event['isBase64Encoded']:
            body = base64.b64decode(body)
        
        # The content type should indicate multipart/form-data
        # Extract the file name and content from the body
        content_type = event['headers']['Content-Type']
        boundary = content_type.split('=')[1]
        parts = body.split(f'--{boundary}'.encode())
        
        # Loop through each part to find the file
        for part in parts:
            if b'Content-Disposition' in part and b'filename=' in part:
                # Get the filename
                header, file_content = part.split(b'\r\n\r\n', 1)
                filename = header.split(b'filename=')[1].split(b'"')[1].decode()
                
                # Clean up the file content by stripping the trailing CRLF
                file_content = file_content.rstrip(b'\r\n--')
                
                # Upload the file to S3
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=unquote_plus(filename),
                    Body=file_content,
                    ContentType='application/octet-stream'  # Change as needed
                )
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'File uploaded successfully!', 'filename': filename})
                }
                
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'File not found in the request'})
        }

    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
