import boto3
import base64
import json

def lambda_handler(event, context):
    # Inicializar el cliente S3
    s3 = boto3.client('s3')

    # Leer el bucket, directorio y el archivo del evento recibido
    nombre_bucket = event['body']['bucket']
    directorio = event['body']['directorio']  # e.g., 'my-folder/'
    file_name = event['body']['file_name']    # e.g., 'example.txt'
    file_content = event['body']['file_content']  # Este será el archivo en base64

    # Convertir el archivo de base64 a binario
    file_data = base64.b64decode(file_content)

    # Si tienes un directorio, sube el archivo en esa carpeta
    key = f"{directorio}{file_name}" if directorio else file_name

    # Subir el archivo a S3
    response = s3.put_object(
        Bucket=nombre_bucket,
        Key=key,
        Body=file_data
    )

    # Salida
    return {
        'statusCode': 200,
        'body': f"File {file_name} uploaded to {key} in {nombre_bucket}."
    }