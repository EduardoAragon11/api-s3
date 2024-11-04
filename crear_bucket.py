import boto3

def lambda_handler(event, context):
    # Entrada: Nombre del bucket desde el evento
    nombre_bucket = event['body']['bucket']

    # Inicializar el cliente S3
    client = boto3.client('s3')

    # Proceso: Crear el bucket con permisos específicos
    response = client.create_bucket(
        Bucket=nombre_bucket,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2'
        },
        # Define ACL using Grants
        GrantFullControl='emailaddress="eduardo.aragon@utec.edu.pe"',  # Replace with the grantee's email or canonical user ID
        ObjectOwnership='BucketOwnerPreferred'  # Optional, based on your ownership preference
    )

    # Salida
    return {
        'statusCode': 200,
        'response': response
    }
