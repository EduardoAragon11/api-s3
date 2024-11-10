import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Bucket name (unique across all AWS accounts)
    bucket_name = 'eaa-new-bucket'  # Change to your desired bucket name
    
    # Define the AWS region
    region = 'us-east-1'  # Change to your desired region
    
    try:
        # Create the S3 bucket
        response = s3_client.create_bucket(
            Bucket=bucket_name
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully created bucket: {bucket_name}')
        }
        
    except ClientError as e:
        return {
            'statusCode': 501,
            'body': json.dumps(f'Error: {e}')
        }
