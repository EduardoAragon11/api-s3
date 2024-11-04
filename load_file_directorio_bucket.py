import boto3
import logging
from requests_toolbelt.multipart import decoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Log the incoming event
        logger.info("Received event: %s", event)

        # Ensure the content type is multipart/form-data
        content_type = event['headers'].get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            return {
                'statusCode': 400,
                'body': 'Content-Type must be multipart/form-data'
            }

        # Decode the form-data
        body = event['body'].encode('utf-8')
        multipart_data = decoder.MultipartDecoder(body, content_type)

        # Extract the necessary parameters
        nombre_bucket = None
        directorio = None
        file_name = None
        file_content = None

        for part in multipart_data.parts:
            if part.headers[b'Content-Disposition']:
                content_disposition = part.headers[b'Content-Disposition'].decode('utf-8')
                if 'name="bucket"' in content_disposition:
                    nombre_bucket = part.text
                elif 'name="directorio"' in content_disposition:
                    directorio = part.text
                elif 'name="file_name"' in content_disposition:
                    file_name = part.text
                elif 'name="file"' in content_disposition:
                    file_content = part.content

        # Validate the extracted fields
        if not nombre_bucket or not file_name or file_content is None:
            return {
                'statusCode': 400,
                'body': 'Missing required form data fields.'
            }

        # Log the parameters
        logger.info("Bucket: %s, Directorio: %s, File Name: %s", nombre_bucket, directorio, file_name)

        # Handle the file upload to S3
        key = f"{directorio}/{file_name}" if directorio else file_name
        s3.put_object(Bucket=nombre_bucket, Key=key, Body=file_content)

        return {
            'statusCode': 200,
            'body': f"File {file_name} uploaded to {key} in {nombre_bucket}."
        }

    except Exception as e:
        logger.error("Error occurred: %s", str(e))
        return {
            'statusCode': 500,
            'body': "Internal server error"
        }
