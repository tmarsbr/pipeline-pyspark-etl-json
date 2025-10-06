# Cria Imagem PySpark

# Imagem do SO usada como base
FROM python:3.11-bullseye as spark-base

# Atualiza o SO e instala pacotes
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      nano \
      unzip \
      rsync \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar variáveis de ambiente para Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Cria as pastas
RUN mkdir -p /opt/hadoop && mkdir -p /opt/spark

# Definir diretório de trabalho
WORKDIR /opt/spark

# Download e instalação do Apache Spark com validação
RUN curl -L --fail --show-error --silent \
    https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz \
    -o spark-3.5.0-bin-hadoop3.tgz && \
    echo "Verificando integridade do arquivo..." && \
    file spark-3.5.0-bin-hadoop3.tgz && \
    tar -tzf spark-3.5.0-bin-hadoop3.tgz >/dev/null && \
    echo "Extraindo Apache Spark..." && \
    tar xzf spark-3.5.0-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 && \
    rm -rf spark-3.5.0-bin-hadoop3.tgz

# Variáveis de ambiente para Spark
ENV SPARK_HOME="/opt/spark"
ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"

# Prepara o ambiente com PySpark
FROM spark-base as pyspark

# Instala as dependências Python
COPY requirements/requirements.txt .
RUN pip3 install -r requirements.txt

# Mais variáveis de ambiente
ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"

# Copia o arquivo de configuração do Spark para a imagem
COPY conf/spark-defaults.conf "$SPARK_HOME/conf"

# Permissões
RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

# Variável PYTHONPATH
ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

# Copia o script de inicialização dos serviços para a imagem
COPY entrypoint.sh .

# Ajusta o privilégio
RUN chmod +x entrypoint.sh

# Executa o script quando inicializar um container
ENTRYPOINT ["./entrypoint.sh"]

# Imagem do Spark Master
FROM spark-base AS spark-master

EXPOSE 8080 7077 6066

CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.master.Master"]

# Imagem do Spark Worker
FROM spark-base AS spark-worker

EXPOSE 8081

CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.worker.Worker", "spark://spark-master:7077"]

# Imagem do History Server
FROM spark-base AS spark-history-server

EXPOSE 18080

CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.history.HistoryServer"]

