"""
Pipeline ETL PySpark para Processar Arquivos JSON

Este script demonstra um pipeline completo de ETL (Extract, Transform, Load)
utilizando PySpark para processar arquivos JSON de diferentes fontes.

Autor: Tiago Mars
Email: tiagomars233@gmail.com
GitHub: https://github.com/tmarsbr
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, lit, to_timestamp, explode, array_contains,
    count, sum as spark_sum, avg, max as spark_max, min as spark_min,
    concat_ws, regexp_replace, upper, lower, trim, coalesce
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType, TimestampType
import sys
from datetime import datetime


class ETLPipeline:
    """
    Classe principal para executar o pipeline ETL de arquivos JSON.
    """
    
    def __init__(self, app_name="Pipeline-ETL-JSON"):
        """
        Inicializa a sessão Spark.
        
        Args:
            app_name (str): Nome da aplicação Spark
        """
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        print(f"[INFO] Sessão Spark iniciada: {app_name}")
    
    def extract_json(self, file_path, multiline=True):
        """
        Extrai dados de arquivo JSON.
        
        Args:
            file_path (str): Caminho do arquivo JSON
            multiline (bool): Se o JSON tem múltiplas linhas
            
        Returns:
            DataFrame: DataFrame com os dados extraídos
        """
        print(f"[EXTRACT] Lendo arquivo: {file_path}")
        try:
            df = self.spark.read.option("multiLine", multiline).json(file_path)
            record_count = df.count()
            print(f"[EXTRACT] Registros extraídos: {record_count}")
            return df
        except Exception as e:
            print(f"[ERROR] Erro ao extrair arquivo {file_path}: {str(e)}")
            return None
    
    def transform_usuarios(self, df):
        """
        Aplica transformações específicas para dados de usuários.
        
        Args:
            df (DataFrame): DataFrame com dados brutos
            
        Returns:
            DataFrame: DataFrame transformado
        """
        print("[TRANSFORM] Aplicando transformações em dados de usuários...")
        
        # Limpeza e validação
        df_transformed = df \
            .filter(col("id").isNotNull()) \
            .withColumn("email", lower(trim(col("email")))) \
            .withColumn("nome", trim(col("nome"))) \
            .withColumn("cidade", trim(col("cidade"))) \
            .withColumn("data_cadastro", to_timestamp(col("data_cadastro"))) \
            .withColumn("idade", when(col("idade").isNull(), 0).otherwise(col("idade"))) \
            .withColumn("email_valido", when(col("email").isNull(), False).otherwise(True)) \
            .withColumn("tags_count", when(col("tags").isNotNull(), 
                                          when(col("tags").cast("string").contains("["), 
                                               col("tags").cast("string").length() - 
                                               regexp_replace(col("tags").cast("string"), "[^,]", "").length() + 1)
                                          .otherwise(0)).otherwise(0))
        
        # Adiciona coluna de categoria de usuário
        df_transformed = df_transformed.withColumn(
            "categoria",
            when(array_contains(col("tags"), "vip"), "VIP")
            .when(array_contains(col("tags"), "premium"), "Premium")
            .otherwise("Standard")
        )
        
        print(f"[TRANSFORM] Transformações aplicadas. Total de registros: {df_transformed.count()}")
        return df_transformed
    
    def transform_transacoes(self, df):
        """
        Aplica transformações específicas para dados de transações.
        
        Args:
            df (DataFrame): DataFrame com dados brutos
            
        Returns:
            DataFrame: DataFrame transformado
        """
        print("[TRANSFORM] Aplicando transformações em dados de transações...")
        
        # Limpeza e enriquecimento
        df_transformed = df \
            .filter(col("transacao_id").isNotNull()) \
            .withColumn("data_transacao", to_timestamp(col("data_transacao"))) \
            .withColumn("status", upper(trim(col("status")))) \
            .withColumn("metodo_tipo", col("metodo_pagamento.tipo")) \
            .withColumn("metodo_bandeira", col("metodo_pagamento.bandeira")) \
            .withColumn("valor_normalizado", col("valor")) \
            .withColumn(
                "status_processamento",
                when(col("status") == "APROVADA", "Concluída")
                .when(col("status") == "RECUSADA", "Rejeitada")
                .otherwise("Em Análise")
            )
        
        # Calcula taxa estimada (simplificado para demonstração)
        df_transformed = df_transformed.withColumn(
            "taxa_estimada",
            when(col("metodo_tipo") == "cartao_credito", col("valor") * 0.03)
            .when(col("metodo_tipo") == "pix", col("valor") * 0.01)
            .otherwise(col("valor") * 0.015)
        )
        
        print(f"[TRANSFORM] Transformações aplicadas. Total de registros: {df_transformed.count()}")
        return df_transformed
    
    def transform_sensores(self, df):
        """
        Aplica transformações específicas para dados de sensores IoT.
        
        Args:
            df (DataFrame): DataFrame com dados brutos
            
        Returns:
            DataFrame: DataFrame transformado
        """
        print("[TRANSFORM] Aplicando transformações em dados de sensores IoT...")
        
        # Limpeza e normalização
        df_transformed = df \
            .filter(col("sensor_id").isNotNull()) \
            .withColumn("timestamp", to_timestamp(col("timestamp"))) \
            .withColumn("tipo", upper(trim(col("tipo")))) \
            .withColumn("status", upper(trim(col("status")))) \
            .withColumn("sala", col("localizacao.sala")) \
            .withColumn("andar", col("localizacao.andar")) \
            .withColumn("predio", col("localizacao.predio")) \
            .withColumn("localizacao_completa", 
                       concat_ws(" - ", col("predio"), col("andar"), col("sala")))
        
        # Adiciona alertas baseados em thresholds
        df_transformed = df_transformed.withColumn(
            "nivel_alerta",
            when((col("tipo") == "TEMPERATURA") & (col("leitura") > 25), "ALTO")
            .when((col("tipo") == "UMIDADE") & (col("leitura") > 70), "ALTO")
            .when(col("status") == "ALERTA", "MEDIO")
            .otherwise("NORMAL")
        )
        
        print(f"[TRANSFORM] Transformações aplicadas. Total de registros: {df_transformed.count()}")
        return df_transformed
    
    def aggregate_data(self, df, group_by_cols, agg_dict):
        """
        Realiza agregações nos dados.
        
        Args:
            df (DataFrame): DataFrame a ser agregado
            group_by_cols (list): Lista de colunas para agrupar
            agg_dict (dict): Dicionário com agregações {coluna: função}
            
        Returns:
            DataFrame: DataFrame agregado
        """
        print(f"[AGGREGATE] Agregando dados por: {', '.join(group_by_cols)}")
        df_agg = df.groupBy(*group_by_cols).agg(**agg_dict)
        print(f"[AGGREGATE] Registros agregados: {df_agg.count()}")
        return df_agg
    
    def load_to_parquet(self, df, output_path, mode="overwrite"):
        """
        Carrega dados em formato Parquet.
        
        Args:
            df (DataFrame): DataFrame a ser salvo
            output_path (str): Caminho de saída
            mode (str): Modo de escrita (overwrite, append)
        """
        print(f"[LOAD] Salvando dados em: {output_path}")
        try:
            df.write.mode(mode).parquet(output_path)
            print(f"[LOAD] Dados salvos com sucesso!")
        except Exception as e:
            print(f"[ERROR] Erro ao salvar dados: {str(e)}")
    
    def load_to_csv(self, df, output_path, mode="overwrite"):
        """
        Carrega dados em formato CSV.
        
        Args:
            df (DataFrame): DataFrame a ser salvo
            output_path (str): Caminho de saída
            mode (str): Modo de escrita (overwrite, append)
        """
        print(f"[LOAD] Salvando dados em CSV: {output_path}")
        try:
            df.write.mode(mode).option("header", "true").csv(output_path)
            print(f"[LOAD] Dados salvos com sucesso!")
        except Exception as e:
            print(f"[ERROR] Erro ao salvar dados: {str(e)}")
    
    def show_statistics(self, df, description="DataFrame"):
        """
        Exibe estatísticas do DataFrame.
        
        Args:
            df (DataFrame): DataFrame para análise
            description (str): Descrição do DataFrame
        """
        print(f"\n{'='*60}")
        print(f"Estatísticas: {description}")
        print(f"{'='*60}")
        print(f"Total de Registros: {df.count()}")
        print(f"Total de Colunas: {len(df.columns)}")
        print(f"\nSchema:")
        df.printSchema()
        print(f"\nPrimeiras 5 linhas:")
        df.show(5, truncate=False)
        print(f"{'='*60}\n")
    
    def stop(self):
        """
        Encerra a sessão Spark.
        """
        print("[INFO] Encerrando sessão Spark...")
        self.spark.stop()


def main():
    """
    Função principal que executa o pipeline ETL.
    """
    print("\n" + "="*60)
    print("Pipeline ETL PySpark - Processamento de Arquivos JSON")
    print("="*60 + "\n")
    
    # Inicializa o pipeline
    etl = ETLPipeline("Pipeline-ETL-JSON-Demo")
    
    # Caminhos dos arquivos
    input_path = "/opt/workspace/dados"
    output_path = "/opt/workspace/output"
    
    try:
        # ============================================================
        # PROCESSAR DADOS DE USUÁRIOS
        # ============================================================
        print("\n[PIPELINE] Processando dados de USUÁRIOS...")
        df_usuarios = etl.extract_json(f"{input_path}/usuarios_api.json")
        
        if df_usuarios:
            etl.show_statistics(df_usuarios, "Usuários - Raw")
            df_usuarios_transformed = etl.transform_usuarios(df_usuarios)
            etl.show_statistics(df_usuarios_transformed, "Usuários - Transformed")
            etl.load_to_parquet(df_usuarios_transformed, f"{output_path}/usuarios")
            etl.load_to_csv(df_usuarios_transformed, f"{output_path}/usuarios_csv")
        
        # ============================================================
        # PROCESSAR DADOS DE TRANSAÇÕES
        # ============================================================
        print("\n[PIPELINE] Processando dados de TRANSAÇÕES...")
        df_transacoes = etl.extract_json(f"{input_path}/transacoes_api.json")
        
        if df_transacoes:
            etl.show_statistics(df_transacoes, "Transações - Raw")
            df_transacoes_transformed = etl.transform_transacoes(df_transacoes)
            etl.show_statistics(df_transacoes_transformed, "Transações - Transformed")
            etl.load_to_parquet(df_transacoes_transformed, f"{output_path}/transacoes")
            
            # Agregação de transações por usuário
            df_trans_agg = etl.aggregate_data(
                df_transacoes_transformed,
                ["usuario_id"],
                {
                    "transacao_id": count("transacao_id").alias("total_transacoes"),
                    "valor": spark_sum("valor").alias("valor_total"),
                    "valor_avg": avg("valor").alias("valor_medio"),
                    "taxa_estimada": spark_sum("taxa_estimada").alias("total_taxas")
                }
            )
            etl.show_statistics(df_trans_agg, "Transações Agregadas por Usuário")
            etl.load_to_parquet(df_trans_agg, f"{output_path}/transacoes_por_usuario")
        
        # ============================================================
        # PROCESSAR DADOS DE SENSORES IoT
        # ============================================================
        print("\n[PIPELINE] Processando dados de SENSORES IoT...")
        df_sensores = etl.extract_json(f"{input_path}/sensores_iot.json")
        
        if df_sensores:
            etl.show_statistics(df_sensores, "Sensores - Raw")
            df_sensores_transformed = etl.transform_sensores(df_sensores)
            etl.show_statistics(df_sensores_transformed, "Sensores - Transformed")
            etl.load_to_parquet(df_sensores_transformed, f"{output_path}/sensores")
            
            # Agregação de leituras por sensor
            df_sensores_agg = etl.aggregate_data(
                df_sensores_transformed,
                ["sensor_id", "tipo"],
                {
                    "leitura": avg("leitura").alias("leitura_media"),
                    "leitura_max": spark_max("leitura").alias("leitura_maxima"),
                    "leitura_min": spark_min("leitura").alias("leitura_minima"),
                    "total_leituras": count("leitura").alias("total_leituras")
                }
            )
            etl.show_statistics(df_sensores_agg, "Sensores Agregados")
            etl.load_to_parquet(df_sensores_agg, f"{output_path}/sensores_agregados")
        
        print("\n" + "="*60)
        print("Pipeline ETL executado com sucesso!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Erro durante a execução do pipeline: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Encerra a sessão Spark
        etl.stop()


if __name__ == "__main__":
    main()
