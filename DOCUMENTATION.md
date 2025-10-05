# Documentação Técnica - Pipeline ETL PySpark

## Visão Geral

Este projeto implementa um pipeline ETL (Extract, Transform, Load) completo usando Apache Spark e Python para processar arquivos JSON de diferentes fontes.

## Arquitetura

### Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    Spark Cluster                         │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ Spark Master │  │ Spark Worker │  │ History Server│ │
│  │   Port 7077  │  │  Port 8081   │  │  Port 18080  │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
           │                    │                 │
           ▼                    ▼                 ▼
┌──────────────────────────────────────────────────────────┐
│                      Workspace                            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │  dados/  │──▶│  jobs/   │──▶│ output/  │            │
│  │  (JSON)  │   │ (PySpark)│   │(Parquet) │            │
│  └──────────┘   └──────────┘   └──────────┘            │
└──────────────────────────────────────────────────────────┘
```

### Fluxo de Dados

1. **Extract**: Leitura de arquivos JSON do diretório `dados/`
2. **Transform**: Aplicação de limpeza, validação e enriquecimento
3. **Load**: Escrita em formato Parquet e CSV no diretório `output/`

## Estrutura de Código

### etl_pipeline.py

Classe principal `ETLPipeline` com os seguintes métodos:

#### Métodos de Extração
- `extract_json(file_path, multiline=True)`: Lê arquivos JSON

#### Métodos de Transformação
- `transform_usuarios(df)`: Transforma dados de usuários
  - Limpeza de emails
  - Tratamento de valores nulos
  - Categorização de usuários
  
- `transform_transacoes(df)`: Transforma dados de transações
  - Normalização de status
  - Extração de campos aninhados
  - Cálculo de taxas
  
- `transform_sensores(df)`: Transforma dados de sensores
  - Normalização de timestamps
  - Criação de alertas
  - Agregação de localizações

#### Métodos de Agregação
- `aggregate_data(df, group_by_cols, agg_dict)`: Agregação genérica

#### Métodos de Carga
- `load_to_parquet(df, output_path, mode)`: Salva em Parquet
- `load_to_csv(df, output_path, mode)`: Salva em CSV

#### Métodos Utilitários
- `show_statistics(df, description)`: Exibe estatísticas
- `stop()`: Encerra sessão Spark

### simple_example.py

Exemplo simplificado demonstrando:
1. Leitura de JSON
2. Transformação básica
3. Escrita em Parquet

## Dados de Entrada

### usuarios_api.json

Representa dados de usuários obtidos de uma API CRM.

**Campos:**
- `id`: Identificador único (integer)
- `nome`: Nome completo (string)
- `email`: Endereço de email (string, pode ser null)
- `idade`: Idade em anos (integer, pode ser null)
- `cidade`: Cidade de residência (string)
- `data_cadastro`: Data/hora do cadastro (timestamp ISO 8601)
- `ativo`: Status ativo (boolean)
- `tags`: Categorias do usuário (array<string>)

**Transformações Aplicadas:**
- Normalização de email para lowercase
- Substituição de idade null por 0
- Criação de flag `email_valido`
- Contagem de tags
- Categorização (VIP, Premium, Standard)

### transacoes_api.json

Representa transações financeiras processadas.

**Campos:**
- `transacao_id`: Identificador único (string)
- `usuario_id`: ID do usuário (integer)
- `valor`: Valor da transação (float)
- `moeda`: Código da moeda (string)
- `data_transacao`: Data/hora da transação (timestamp)
- `status`: Status da transação (string)
- `metodo_pagamento`: Objeto com detalhes do pagamento
  - `tipo`: Tipo de pagamento (string)
  - `bandeira`: Bandeira do cartão (string, opcional)
  - `ultimos_digitos`: Últimos dígitos (string, opcional)
  - `chave`: Tipo de chave PIX (string, opcional)

**Transformações Aplicadas:**
- Normalização de status para uppercase
- Extração de campos do objeto aninhado
- Cálculo de taxa estimada por tipo de pagamento
- Criação de campo `status_processamento`

### sensores_iot.json

Representa leituras de sensores IoT em datacenters.

**Campos:**
- `sensor_id`: Identificador do sensor (string)
- `tipo`: Tipo de medição (string: temperatura, umidade)
- `localizacao`: Objeto com localização física
  - `sala`: Nome da sala (string)
  - `andar`: Número do andar (integer)
  - `predio`: Nome do prédio (string)
- `leitura`: Valor medido (float)
- `unidade`: Unidade de medida (string)
- `timestamp`: Data/hora da leitura (timestamp)
- `status`: Status da leitura (string)

**Transformações Aplicadas:**
- Normalização de tipo para uppercase
- Extração de campos de localização
- Criação de campo `localizacao_completa`
- Criação de `nivel_alerta` baseado em thresholds

## Dados de Saída

### Formato Parquet

Formato colunar otimizado para:
- Queries analíticas
- Compressão eficiente
- Integração com ferramentas de big data

**Vantagens:**
- Ocupa menos espaço
- Leitura mais rápida de colunas específicas
- Mantém schema dos dados
- Compressão nativa

### Formato CSV

Formato texto com separadores para:
- Compatibilidade universal
- Fácil visualização
- Importação em Excel/ferramentas simples

## Configurações

### config_example.py

Arquivo de configuração com:
- Parâmetros do Spark
- Conexões de banco de dados (PostgreSQL, MongoDB, MySQL)
- Thresholds de alertas
- Taxas de transação
- Configurações de performance

**Uso:**
1. Copie `config_example.py` para `config.py`
2. Ajuste as configurações conforme necessário
3. Importe no seu script: `from config import *`

## Performance

### Otimizações Implementadas

1. **Adaptive Query Execution**: Habilitado no Spark
2. **Coalesce Partitions**: Reduz partições desnecessárias
3. **Caching**: Usa cache quando reutiliza DataFrames
4. **Particionamento**: Suporta particionamento na escrita

### Escalabilidade

- **Vertical**: Aumente memória dos workers no docker-compose.yml
- **Horizontal**: Escale número de workers: `docker compose up -d --scale spark-worker=N`

### Benchmarks Esperados

Com configuração padrão (1 worker, 1GB RAM):
- 1.000 registros JSON: ~5 segundos
- 10.000 registros JSON: ~15 segundos
- 100.000 registros JSON: ~60 segundos

## Extensões Possíveis

### Integração com Bancos de Dados

```python
# PostgreSQL
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "schema.table") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("append") \
    .save()
```

### Streaming

```python
# Processar JSONs em tempo real
df_stream = spark \
    .readStream \
    .schema(schema) \
    .json("path/to/json/stream")

query = df_stream \
    .writeStream \
    .format("parquet") \
    .option("path", "output/path") \
    .option("checkpointLocation", "checkpoint/path") \
    .start()
```

### Particionamento

```python
# Particionar por data
df.write \
    .partitionBy("data_processamento") \
    .parquet("output/path")
```

## Testes

### Testes Unitários (Futuro)

```python
import unittest
from etl_pipeline import ETLPipeline

class TestETLPipeline(unittest.TestCase):
    def setUp(self):
        self.etl = ETLPipeline("test-app")
    
    def test_extract_json(self):
        df = self.etl.extract_json("test_data.json")
        self.assertIsNotNone(df)
```

### Testes de Integração

1. Executar pipeline com dados de teste
2. Verificar estrutura dos arquivos de saída
3. Validar contagem de registros
4. Verificar qualidade dos dados

## Monitoramento

### Spark UI

- **URL**: http://localhost:9091
- **Informações**:
  - Jobs em execução
  - Estágios completados
  - Uso de memória
  - Tarefas por executor

### History Server

- **URL**: http://localhost:18081
- **Informações**:
  - Histórico de aplicações
  - Estatísticas de execução
  - Logs de jobs anteriores

### Logs

```bash
# Ver logs em tempo real
docker logs -f spark-master

# Ver últimas 100 linhas
docker logs --tail 100 spark-master
```

## Troubleshooting

### Erro: Out of Memory

**Solução**: Aumente memória dos workers

```yaml
environment:
  - SPARK_WORKER_MEMORY=2G
  - SPARK_EXECUTOR_MEMORY=1G
```

### Erro: JSON parse error

**Solução**: Valide JSON com ferramentas online
- Use JSONLint: https://jsonlint.com/
- Verifique encoding (deve ser UTF-8)

### Erro: Container não inicia

**Solução**: Verifique logs e portas
```bash
docker compose logs
netstat -an | grep 9091
```

## Boas Práticas

1. **Sempre valide JSONs** antes de processar
2. **Use schemas explícitos** para dados críticos
3. **Implemente tratamento de erros** robusto
4. **Monitore uso de recursos** durante execução
5. **Documente transformações** aplicadas
6. **Versione schemas** de dados
7. **Teste com dados reais** antes de produção

## Referências

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Licença

Este projeto é de código aberto e pode ser usado como base para seus próprios projetos.

---

**Autor**: Tiago Mars  
**Contato**: tiagomars233@gmail.com  
**GitHub**: [@tmarsbr](https://github.com/tmarsbr)
