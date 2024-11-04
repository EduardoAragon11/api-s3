import boto3

def lambda_handler(event, context):
    # Entrada
    nombre_bucket = event['body']['bucket']

    # Inicializar el cliente S3
    client = boto3.client('s3')

    # Proceso: Crear el bucket
    response = client.create_bucket(
        Bucket=nombre_bucket,
        GrantFullControl='id=634152101290',
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-1'
        },
        ObjectOwnership='BucketOwnerPreferred'
    )

    # Salida
    return {
        'statusCode': 200,
        'response': response
    }
