import boto3

def lambda_handler(event, context):
    # Entrada
    nombre_bucket = event['body']['bucket']

    # Inicializar el cliente S3
    client = boto3.client('s3')

    # Proceso: Crear el bucket
    response = client.create_bucket(
        Bucket=nombre_bucket,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-1'  # Cambiar si se necesita otra región
        }
    )

    # Desbloquear el acceso público al bucket
    client.put_public_access_block(
        Bucket=nombre_bucket,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )

    # Salida
    return {
        'statusCode': 200,
        'response': response
    }
