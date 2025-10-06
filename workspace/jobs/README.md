# Jobs - Scripts PySpark ETL

Esta pasta contém os scripts PySpark para processamento de arquivos JSON.

## Scripts Disponíveis

### 1. etl_pipeline.py
Pipeline ETL completo que demonstra:
- Extração de múltiplos arquivos JSON
- Transformações complexas (limpeza, validação, enriquecimento)
- Agregações e estatísticas
- Carregamento em formato Parquet e CSV

**Como executar:**
```bash
# Via Spark Submit
spark-submit /opt/workspace/jobs/etl_pipeline.py

# Ou dentro do container
docker exec -it spark-master spark-submit /opt/workspace/jobs/etl_pipeline.py
```

### 2. simple_example.py
Exemplo simplificado para demonstração rápida do conceito ETL.

**Como executar:**
```bash
# Via Spark Submit
spark-submit /opt/workspace/jobs/simple_example.py

# Ou dentro do container
docker exec -it spark-master spark-submit /opt/workspace/jobs/simple_example.py
```

## Estrutura do Pipeline

```
Extract → Transform → Load
   ↓          ↓         ↓
JSON    Limpeza    Parquet/CSV
        Validação
        Agregação
```

## Dados de Entrada

Os scripts processam arquivos JSON da pasta `/opt/workspace/dados/`:
- `usuarios_api.json` - Dados de usuários
- `transacoes_api.json` - Dados de transações financeiras
- `sensores_iot.json` - Leituras de sensores IoT

## Dados de Saída

Os resultados são salvos em `/opt/workspace/output/`:
- Formato Parquet (otimizado para analytics)
- Formato CSV (para compatibilidade)

## Requisitos

- PySpark 3.5.0+
- Python 3.11+
- Spark Cluster ativo (via docker-compose)
