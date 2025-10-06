"""
Script de Exemplo Simples - Pipeline ETL JSON

Este é um exemplo simplificado para demonstrar rapidamente
o processamento de arquivos JSON com PySpark.

Autor: Tiago Mars
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, upper

# Cria sessão Spark
spark = SparkSession.builder \
    .appName("ETL-Simple-Example") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("\n" + "="*50)
print("Exemplo Simples - ETL de Arquivos JSON")
print("="*50 + "\n")

# EXTRACT: Lê arquivo JSON
print("[1] Extraindo dados...")
df = spark.read.option("multiLine", True).json("/opt/workspace/dados/usuarios_api.json")
print(f"   Registros lidos: {df.count()}")

# TRANSFORM: Aplica transformações
print("\n[2] Transformando dados...")
df_transformed = df \
    .filter(col("id").isNotNull()) \
    .withColumn("data_cadastro", to_timestamp(col("data_cadastro"))) \
    .withColumn("cidade_upper", upper(col("cidade")))

print(f"   Registros após transformação: {df_transformed.count()}")

# Exibe resultado
print("\n[3] Visualizando dados transformados:")
df_transformed.select("id", "nome", "cidade", "cidade_upper", "data_cadastro").show(5)

# LOAD: Salva resultado
print("\n[4] Salvando dados transformados...")
df_transformed.write.mode("overwrite").parquet("/opt/workspace/output/usuarios_simple")
print("   Dados salvos em: /opt/workspace/output/usuarios_simple")

print("\n" + "="*50)
print("Processamento concluído!")
print("="*50 + "\n")

spark.stop()
