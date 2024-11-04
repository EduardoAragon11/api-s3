import boto3

def lambda_handler(event, context):
    # Entrada
    nombre_bucket = event['body']['bucket']
    directorio = event['body']['directorio']

    # Inicializar el cliente S3
    client = boto3.client('s3')

    response = client.put_object(
        Bucket=nombre_bucket,
        Key=directorio  # 'my-folder/' (terminado en '/')
    )

    # Salida
    return {
        'statusCode': 200,
        'response': response
    }
