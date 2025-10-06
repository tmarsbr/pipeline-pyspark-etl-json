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

1. **Pré-requisitos**: Docker, Docker Compose e Python instalados.
2. **Configurar Ambiente**:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```
3. **Executar Pipeline**:
   - Coloque arquivos JSON na pasta `dados/`.
   - Execute o script PySpark em `jobs/` via Spark Submit.
4. **Verificar Resultados**: Dados carregados no banco configurado.

### Erros Comuns e Soluções Encontradas Durante o Desenvolvimento

Durante a implementação e testes do pipeline, enfrentei vários desafios técnicos que são comuns em projetos com Docker, PySpark e bancos de dados. Aqui estão os principais erros e como foram resolvidos:

1. **Erro: "No such container: dsa-pyspark-master"**
   - **Causa**: Nome do container incorreto no comando `docker exec`.
   - **Solução**: Corrigir o nome para `spark-master` conforme definido no `docker-compose.yml`.

2. **Erro: "spark-submit: command not found"**
   - **Causa**: Variáveis de ambiente `SPARK_HOME` e `PATH` não configuradas no Dockerfile.
   - **Solução**: Adicionar `ENV SPARK_HOME=/opt/spark` e `ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin` no estágio `spark-base` do Dockerfile.

3. **Erro: Caminhos relativos não funcionam no container**
   - **Causa**: Scripts PySpark usando caminhos como `'data/usuarios.json'` em vez de absolutos.
   - **Solução**: Alterar para caminhos absolutos como `/opt/workspace/dados/usuarios.json`, já que o volume é montado em `/opt/workspace`.

4. **Erro: Volume mount incorreto**
   - **Causa**: `docker-compose.yml` montando apenas subpastas em vez do projeto inteiro.
   - **Solução**: Mudar de `./dados:/opt/workspace/dados` para `.:/opt/workspace` para montar todo o projeto.

5. **Erro: "readonly database" ao gravar no SQLite**
   - **Causa**: Arquivo `usuarios.db` com atributo ReadOnly no sistema de arquivos Windows.
   - **Solução**: Usar PowerShell para remover o atributo: `Set-ItemProperty -Path "dados\usuarios.db" -Name IsReadOnly -Value $false`. Reiniciar containers para refletir mudanças.

6. **Erro: Falta do driver JDBC para SQLite**
   - **Causa**: PySpark tentando conectar ao SQLite sem o driver JDBC.
   - **Solução**: Adicionar `--jars /opt/workspace/dados/sqlite-jdbc-3.44.1.0.jar` ao comando `spark-submit`.

Essas correções garantiram que o pipeline funcionasse end-to-end, processando JSONs, aplicando filtros (idade >35, cidade=Natal, salário<7000) e carregando dados no SQLite via JDBC.

### Resultados e Aprendizados

Este pipeline não apenas processa JSONs eficientemente, mas me ensinou sobre otimização de queries Spark, tratamento de erros em ETL e design de esquemas de dados. É uma demonstração prática de como transformar desafios de dados em soluções produtivas.

### Próximos Passos

Estou expandindo com streaming em tempo real, integração com Kafka e dashboards de monitoramento.

### Sobre Mim

Sou um engenheiro de dados apaixonado por tecnologia e resolução de problemas. Busco oportunidades onde possa contribuir com minha expertise em big data e analytics. Vamos conversar?

- **LinkedIn**: [linkedin.com/in/tiago-dados](https://linkedin.com/in/tiago-dados)
- **GitHub**: [tmarsbr](https://github.com/tmarsbr)
- **Email**: tiagomars233@gmail.com

Obrigado por explorar meu projeto. Espero que ele inspire você tanto quanto me inspirou a criá-lo!