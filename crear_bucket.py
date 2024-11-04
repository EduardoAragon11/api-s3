import boto3

def lambda_handler(event, context):
    # Entrada: Nombre del bucket desde el evento
    nombre_bucket = event['body']['bucket']

    # Inicializar el cliente S3
    client = boto3.client('s3')

    # Proceso: Crear el bucket con ACL de acceso público
    response = client.create_bucket(
        ACL='public-read-write',  # Permitir acceso público a leer y escribir
        Bucket=nombre_bucket,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2'
        }
    )

    # Crear una política de bucket para permitir acceso público a todos los objetos
    public_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{nombre_bucket}/*"
            }
        ]
    }

    # Asignar la política pública al bucket
    client.put_bucket_policy(
        Bucket=nombre_bucket,
        Policy=json.dumps(public_policy)
    )

    # Salida
    return {
        'statusCode': 200,
        'response': response
    }
