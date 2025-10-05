# Pipeline PySpark Para Extrair, Transformar e Carregar Arquivos JSON em Banco de Dados

## A Jornada de um Engenheiro de Dados

Olá, recrutador! Bem-vindo ao meu portfólio de engenharia de dados. Este projeto representa minha paixão por construir pipelines robustos de ETL (Extract, Transform, Load), utilizando PySpark para processar arquivos JSON e carregá-los em bancos de dados. Aqui, conto a história de como desenvolvi uma solução eficiente para lidar com dados semi-estruturados, enfrentando desafios comuns em projetos de big data e aplicando melhores práticas de engenharia.

### O Cenário Inicial

Imagine uma empresa que coleta dados de APIs, logs de aplicações ou sensores IoT, todos em formato JSON. Esses dados precisam ser extraídos, limpos, transformados e carregados em um banco de dados relacional ou NoSQL para análises posteriores. Como engenheiro de dados, meu desafio era criar um pipeline escalável que pudesse processar grandes volumes de JSONs, garantindo integridade, performance e facilidade de manutenção.

### Os Desafios Enfrentados

1. **Estrutura Semi-Estruturada**: Como lidar com JSONs aninhados e inconsistentes sem perder dados?
2. **Escalabilidade**: Como processar milhares de arquivos JSON em paralelo?
3. **Transformações Complexas**: Como aplicar regras de negócio durante a transformação?
4. **Integração com Bancos**: Como carregar dados transformados de forma eficiente em diferentes tipos de bancos?

### A Solução Implementada

Utilizei PySpark para criar um pipeline ETL distribuído. A extração lê arquivos JSON de diretórios ou streams, a transformação aplica limpeza e mapeamento usando DataFrames do Spark, e o carregamento insere os dados em bancos como PostgreSQL ou MongoDB. O ambiente foi containerizado com Docker para facilitar testes e deploy.

**Arquitetura Principal:**
- **PySpark**: Extração e transformação de JSONs em DataFrames.
- **Transformações**: Limpeza, validação e agregações.
- **Carregamento**: Inserção em bancos de dados via JDBC ou APIs.
- **Docker**: Ambiente isolado para execução.

**Estrutura do Projeto:**
```
pipeline-pyspark-etl-json/
├── workspace/
│   ├── dados/              # Arquivos JSON de entrada
│   │   ├── usuarios_api.json
│   │   ├── transacoes_api.json
│   │   └── sensores_iot.json
│   ├── jobs/               # Scripts PySpark
│   │   ├── etl_pipeline.py        # Pipeline completo
│   │   ├── simple_example.py      # Exemplo simples
│   │   └── config_example.py      # Configurações
│   ├── output/             # Dados processados (Parquet/CSV)
│   └── spark-logs/         # Logs do Spark
├── docker-compose.yml      # Configuração do cluster
├── Dockerfile              # Imagem Spark customizada
└── run_pipeline.sh         # Script helper para execução
```

### Tecnologias Demonstradas

- **Apache Spark (PySpark)**: Processamento distribuído e manipulação de DataFrames.
- **JSON Handling**: Parsing e transformação de dados semi-estruturados.
- **Bancos de Dados**: Integração com SQL/NoSQL (ex.: PostgreSQL, MongoDB).
- **Docker & Docker Compose**: Containerização para reprodutibilidade.
- **Python**: Scripts para orquestração e lógica de negócio.

Este projeto mostra minha habilidade em:
- Desenvolver pipelines ETL escaláveis.
- Trabalhar com dados semi-estruturados (JSON).
- Integrar Spark com bancos de dados.
- Resolver problemas de performance em big data.

### Como Executar o Projeto

1. **Pré-requisitos**: Docker e Docker Compose instalados.

2. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/tmarsbr/pipeline-pyspark-etl-json.git
   cd pipeline-pyspark-etl-json
   ```

3. **Iniciar o Cluster Spark**:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```
   
   Aguarde alguns segundos para o cluster inicializar. Acesse:
   - Spark Master UI: http://localhost:9091
   - History Server: http://localhost:18081

4. **Executar o Pipeline**:
   
   **Opção 1 - Script Automatizado (Recomendado):**
   ```bash
   # Pipeline completo
   ./run_pipeline.sh full
   
   # Exemplo simples
   ./run_pipeline.sh simple
   ```
   
   **Opção 2 - Manual via Docker:**
   ```bash
   # Pipeline completo
   docker exec -it spark-master spark-submit \
     --master spark://spark-master:7077 \
     /opt/workspace/jobs/etl_pipeline.py
   
   # Exemplo simples
   docker exec -it spark-master spark-submit \
     --master spark://spark-master:7077 \
     /opt/workspace/jobs/simple_example.py
   ```

5. **Verificar Resultados**: 
   - Dados processados salvos em: `workspace/output/`
   - Formato Parquet (otimizado) e CSV (compatibilidade)
   - Logs disponíveis na saída do terminal

6. **Parar o Cluster**:
   ```bash
   docker-compose down
   ```

### Resultados e Aprendizados

Este pipeline não apenas processa JSONs eficientemente, mas me ensinou sobre otimização de queries Spark, tratamento de erros em ETL e design de esquemas de dados. É uma demonstração prática de como transformar desafios de dados em soluções produtivas.

**O que o Pipeline Faz:**

1. **Processa 3 tipos de dados JSON:**
   - Usuários de APIs (com dados faltantes e arrays)
   - Transações financeiras (com estruturas aninhadas)
   - Leituras de sensores IoT (séries temporais)

2. **Aplica transformações avançadas:**
   - Limpeza e normalização de dados
   - Tratamento de valores nulos
   - Extração de campos de JSONs aninhados
   - Criação de novas métricas e categorias
   - Agregações e estatísticas

3. **Gera saídas estruturadas:**
   - Formato Parquet (colunar, otimizado para analytics)
   - Formato CSV (compatibilidade com outras ferramentas)
   - Dados agregados por diferentes dimensões

4. **Demonstra boas práticas:**
   - Código modular e reutilizável
   - Logging e monitoramento
   - Tratamento de erros
   - Configurações externalizadas

### Próximos Passos

Estou expandindo com streaming em tempo real, integração com Kafka e dashboards de monitoramento.

### Sobre Mim

Sou um engenheiro de dados apaixonado por tecnologia e resolução de problemas. Busco oportunidades onde possa contribuir com minha expertise em big data e analytics. Vamos conversar?

- **LinkedIn**: [linkedin.com/in/tiago-dados](https://linkedin.com/in/tiago-dados)
- **GitHub**: [tmarsbr](https://github.com/tmarsbr)
- **Email**: tiagomars233@gmail.com

Obrigado por explorar meu projeto. Espero que ele inspire você tanto quanto me inspirou a criá-lo!