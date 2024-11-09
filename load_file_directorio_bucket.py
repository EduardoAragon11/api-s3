import json
import boto3
import base64

def lambda_handler(event, context):
    client = boto3.client("s3")
    get_file_content = event["content"]
    decode_content = base64.b64decode(get_file_content)
    bucket_name = "eaa-documentos-compras"
    s3_upload = client.put_object(Bucket=bucket_name,Key="data.pdf",Body=decode_content)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('The Object is Uploaded successfully!')
    }
