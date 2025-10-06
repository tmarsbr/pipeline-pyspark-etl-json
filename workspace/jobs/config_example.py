# Configurações do Pipeline ETL
# Renomeie este arquivo para config.py e ajuste conforme necessário

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================
APP_NAME = "Pipeline-ETL-JSON"
LOG_LEVEL = "WARN"  # DEBUG, INFO, WARN, ERROR

# ============================================================
# CAMINHOS DE ARQUIVOS
# ============================================================
INPUT_PATH = "/opt/workspace/dados"
OUTPUT_PATH = "/opt/workspace/output"
CHECKPOINT_PATH = "/opt/workspace/checkpoints"

# ============================================================
# CONFIGURAÇÕES DO SPARK
# ============================================================
SPARK_CONFIG = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.shuffle.partitions": "10",
    "spark.default.parallelism": "8"
}

# ============================================================
# CONFIGURAÇÕES DE BANCO DE DADOS
# ============================================================

# PostgreSQL (exemplo)
POSTGRES_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/pipeline_db",
    "driver": "org.postgresql.Driver",
    "user": "postgres",
    "password": "senha_segura",
    "table": "etl_results"
}

# MongoDB (exemplo)
MONGODB_CONFIG = {
    "uri": "mongodb://localhost:27017",
    "database": "pipeline_db",
    "collection": "etl_results"
}

# MySQL (exemplo)
MYSQL_CONFIG = {
    "url": "jdbc:mysql://localhost:3306/pipeline_db",
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "root",
    "password": "senha_segura",
    "table": "etl_results"
}

# ============================================================
# CONFIGURAÇÕES DE TRANSFORMAÇÃO
# ============================================================

# Thresholds para alertas de sensores
SENSOR_THRESHOLDS = {
    "temperatura_alta": 25.0,
    "temperatura_baixa": 18.0,
    "umidade_alta": 70.0,
    "umidade_baixa": 40.0
}

# Categorias de usuários
USER_CATEGORIES = {
    "vip": "VIP",
    "premium": "Premium",
    "standard": "Standard"
}

# Taxas de processamento de transações (%)
TRANSACTION_FEES = {
    "cartao_credito": 0.03,  # 3%
    "pix": 0.01,             # 1%
    "boleto": 0.015,         # 1.5%
    "default": 0.02          # 2%
}

# ============================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================
BATCH_SIZE = 1000
WRITE_MODE = "overwrite"  # overwrite, append, ignore, error
PARTITION_COLS = ["data_processamento"]  # Colunas para particionar
COALESCE_PARTITIONS = 1  # Número de partições na saída

# ============================================================
# OBSERVAÇÕES
# ============================================================
# - Nunca commite senhas em produção! Use variáveis de ambiente ou secret managers
# - Ajuste os parâmetros de performance conforme o tamanho do cluster
# - Revise os thresholds com base nos requisitos de negócio
