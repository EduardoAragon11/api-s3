import boto3

def lambda_handler(event, context):

	bucket_name = "eaa-documentos-compras"
	prefix = "probando/"

	s3_client = boto3.client('s3')

	open('/tmp/hello.txt', 'w+').write('Hello, world!')

	s3_client.upload_file('/tmp/hello.txt', bucket_name, prefix+'hello-remote.txt')

	return {
        'statusCode': 200,
        'bucket': bucket_name,
        'message': "Created on " + prefix
    }
