#!/bin/bash
#
# Script para executar o pipeline ETL PySpark
#
# Uso:
#   ./run_pipeline.sh [simple|full]
#
# Exemplos:
#   ./run_pipeline.sh simple  # Executa exemplo simples
#   ./run_pipeline.sh full    # Executa pipeline completo
#   ./run_pipeline.sh         # Executa pipeline completo (padrão)

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Pipeline ETL PySpark - Executor${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Verifica se o container do Spark Master está rodando
if ! docker ps | grep -q spark-master; then
    echo -e "${YELLOW}[AVISO] Container spark-master não está rodando!${NC}"
    echo -e "${YELLOW}Iniciando cluster Spark...${NC}\n"
    docker compose -f docker-compose.yml up -d
    echo -e "\n${GREEN}Aguardando cluster inicializar (15 segundos)...${NC}"
    sleep 15
fi

# Define qual script executar
SCRIPT_TYPE=${1:-full}

if [ "$SCRIPT_TYPE" = "simple" ]; then
    echo -e "${GREEN}[INFO] Executando exemplo simples...${NC}\n"
    SCRIPT="/opt/workspace/jobs/simple_example.py"
else
    echo -e "${GREEN}[INFO] Executando pipeline completo...${NC}\n"
    SCRIPT="/opt/workspace/jobs/etl_pipeline.py"
fi

# Executa o script no container do Spark Master
docker exec -it spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    $SCRIPT

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}================================================${NC}"
    echo -e "${GREEN}  Pipeline executado com sucesso!${NC}"
    echo -e "${GREEN}================================================${NC}\n"
    echo -e "${BLUE}[INFO] Resultados salvos em: workspace/output/${NC}\n"
else
    echo -e "\n${YELLOW}================================================${NC}"
    echo -e "${YELLOW}  Erro na execução do pipeline${NC}"
    echo -e "${YELLOW}================================================${NC}\n"
fi

exit $EXIT_CODE
