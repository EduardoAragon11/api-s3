import boto3

def lambda_handler(event, context):
    # Entrada
    nombre_bucket = event['body']['bucket']

    # Inicializar el cliente S3
    client = boto3.client('s3', region_name='us-east-1')

    # Proceso: Crear el bucket
    response = client.create_bucket(
        ACL='public-read-write',
        Bucket=nombre_bucket,
    )

    # Salida
    return {
        'statusCode': 200,
        'response': response
    }
