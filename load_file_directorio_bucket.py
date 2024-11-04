import json
import logging
import boto3
import os
import base64
import re
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Lambda function to upload a file to S3 from a form-data POST request"""

    bucket_name = "eaa-catalogo-productos"

    try:
        # Extract content-type from headers (to validate multipart/form-data)
        content_type = event['headers']['content-type']
        
        if "multipart/form-data" not in content_type:
            raise ValueError("Unsupported content type")
        
        # Get boundary string from content-type
        boundary = content_type.split("boundary=")[1]

        # Split the body using the boundary
        parts = event['body'].split(boundary)

        # Find the part that contains the file
        file_part = None
        for part in parts:
            if 'Content-Disposition: form-data; name="file"' in part:
                file_part = part
                break
        
        if not file_part:
            raise ValueError("File part not found in the request")
        
        # Extract the file content from the multipart section (after the empty line)
        file_data = file_part.split("\r\n\r\n")[1].split("\r\n")[0]

        # Decode the base64 encoded file
        file_data = base64.b64decode(file_data)

        # Define file name, you can change this to extract from form-data if needed
        file_name = "uploaded_file"

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
    except Exception as e:
        logging.error(e)
        return {
            "statusCode": 400,
            "body": json.dumps(f"Error: {str(e)}")
        }
