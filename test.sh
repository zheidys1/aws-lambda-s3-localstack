#!/bin/bash
set -e

# Variáveis de ambiente já definidas no deploy.sh, mas repetidas para clareza
API_ENDPOINT="http://localhost:4566"
API_PROFILE="localstack"
BUCKET_NAME="meu-primeiro-bucket-local"
TABLE_NAME="NotasFiscais"
TEST_FILE="nota-automatica.json"
NOTA_ID="nota-automatica"

echo "--- Iniciando Teste de Fluxo Automatizado ---"

# 1. Cria o arquivo de teste
echo "1. Criando arquivo de teste: $TEST_FILE"
echo '{"numero": "999", "cliente": "Teste Automatizado", "valor": 100.00, "data": "2025-11-01"}' > $TEST_FILE

# 2. Faz o upload (Dispara a Lambda)
echo "2. Fazendo upload para S3 (Isso acionará a Lambda)..."
aws s3 cp $TEST_FILE s3://$BUCKET_NAME/$NOTA_ID.json     --endpoint-url $API_ENDPOINT     --profile $API_PROFILE

# 3. Verifica o DynamoDB (CORREÇÃO: Usando sintaxe robusta para passar JSON com variáveis)
echo "3. Verificando DynamoDB (Procurando por $NOTA_ID)..."
sleep 2 # Dá tempo para a Lambda executar

# Este comando deve retornar o item salvo pela Lambda
aws dynamodb get-item     --table-name ""     --key "{\"NumeroNota\": {\"S\": \"\"}}"     --endpoint-url ""     --profile ""

echo "--- Teste Concluído! O JSON acima confirma o sucesso do fluxo. ---"
