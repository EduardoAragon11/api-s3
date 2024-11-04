import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Log the incoming event
        logger.info("Received event: %s", event)

        # Extract the necessary parameters
        nombre_bucket = event['body']['bucket']
        directorio = event['body']['directorio']
        file_name = event['body']['file_name']
        file_content = event['body']['file_content']

        # Log the parameters
        logger.info("Bucket: %s, Directorio: %s, File Name: %s", nombre_bucket, directorio, file_name)

        # Handle the file upload to S3
        key = f"{directorio}{file_name}" if directorio else file_name
        response = s3.put_object(Bucket=nombre_bucket, Key=key, Body=file_content)

        return {
            'statusCode': 200,
            'body': f"File {file_name} uploaded to {key} in {nombre_bucket}."
        }

    except Exception as e:
        logger.error("Error occurred: %s", str(e))
        return {
            'statusCode': 500,
            'body': "Internal server error",
            'error': e
        }
