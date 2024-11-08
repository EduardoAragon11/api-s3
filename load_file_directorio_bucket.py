import boto3

def lambda_handler(event, context):
    bucket_name = "eaa-documentos-compras"
    prefix = "probando/"
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Create a file in /tmp
    file_path = '/tmp/hello.txt'
    try:
        with open(file_path, 'w+') as file:
            file.write('Hello, world!')
        
        # Upload the file to S3
        s3_client.upload_file(file_path, bucket_name, prefix + 'hello-remote.txt')
        
        return {
            'statusCode': 200,
            'bucket': bucket_name,
            'message': f"File uploaded successfully to {prefix}."
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'message': "File upload failed."
        }
