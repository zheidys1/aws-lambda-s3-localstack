import json
import boto3
import os

# Configura o cliente DynamoDB para o LocalStack, usando o endpoint padrão do Docker
dynamodb = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT', 'http://localstack:4566')
)
TABLE_NAME = 'NotasFiscais' 

def handler(event, context):
    try:
        # Pega a informação do evento S3 (bucket e chave do arquivo)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Novo arquivo detectado no bucket: {bucket} com chave: {key}")

        # O NumeroNota será a chave do arquivo (ex: 'nota-123.json' vira 'nota-123')
        # Este valor será usado como HASH key no DynamoDB
        nota_id = key.replace(".json", "") 
        
        # Grava os dados simplificados no DynamoDB
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'NumeroNota': {'S': nota_id},
                'Status': {'S': 'Processado com Sucesso'},
                'BucketOrigem': {'S': bucket},
                'DataProcessamento': {'S': context.get_remaining_time_in_millis().__str__()} # Apenas um dado extra
            }
        )
        print(f"Item {nota_id} salvo no DynamoDB.")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Processamento concluído!')
        }
    except Exception as e:
        print(f"Erro no processamento: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro: {str(e)}')
        }
