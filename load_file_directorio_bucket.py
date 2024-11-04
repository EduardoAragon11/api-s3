import json
import logging
import boto3
import os
import base64
from botocore.exceptions import ClientError
from urllib.parse import parse_qs

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Lambda function to upload a file to S3 from a form-data POST request

    :param event: API Gateway Lambda Proxy Input Format (contains the uploaded file)
    :param context: Lambda Context runtime methods and attributes
    :return: The response to the API Gateway
    """
    
    bucket_name = "eaa-catalogo-productos"

    try:
        # Extract the content-type from headers
        content_type = event['headers']['content-type']
        
        # Get the file content from the event (API Gateway sends base64-encoded data)
        file_data = base64.b64decode(event['body'])
        
        # For form-data processing, we need to extract the file from the body
        # Assuming the file is under a key like "file" in the form-data
        file_name = "uploaded_file"  # Define a file name or extract from form-data
        
        # Upload the file to S3
        response = s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_data)
        
        return {
            "statusCode": 200,
            "body": json.dumps("File uploaded successfully!")
        }

    except ClientError as e:
        logging.error(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"File upload failed: {str(e)}")
        }
