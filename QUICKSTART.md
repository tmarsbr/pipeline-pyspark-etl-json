# Guia Rápido - Pipeline PySpark ETL JSON

## 🚀 Início Rápido

### 1. Clone o Repositório
```bash
git clone https://github.com/tmarsbr/pipeline-pyspark-etl-json.git
cd pipeline-pyspark-etl-json
```

### 2. Inicie o Cluster Spark
```bash
docker compose up -d
```

### 3. Execute o Pipeline
```bash
# Opção mais fácil - script automatizado
./run_pipeline.sh

# Ou exemplo simples
./run_pipeline.sh simple
```

### 4. Veja os Resultados
```bash
# Listar arquivos de saída
ls -lh workspace/output/

# Ver estrutura dos dados processados
tree workspace/output/
```

### 5. Parar o Cluster
```bash
docker compose down
```

## 📊 O Que Esperar

### Dados de Entrada
- `workspace/dados/usuarios_api.json` - 5 usuários
- `workspace/dados/transacoes_api.json` - 5 transações
- `workspace/dados/sensores_iot.json` - 5 leituras de sensores

### Dados de Saída (após execução)
- `workspace/output/usuarios/` - Usuários transformados (Parquet)
- `workspace/output/usuarios_csv/` - Usuários transformados (CSV)
- `workspace/output/transacoes/` - Transações transformadas (Parquet)
- `workspace/output/transacoes_por_usuario/` - Agregações por usuário
- `workspace/output/sensores/` - Sensores transformados (Parquet)
- `workspace/output/sensores_agregados/` - Estatísticas dos sensores

## 🔍 Verificar Status do Cluster

### Spark Master UI
Abra no navegador: http://localhost:9091

### History Server
Abra no navegador: http://localhost:18081

### Via Terminal
```bash
# Ver containers rodando
docker ps

# Ver logs do master
docker logs spark-master

# Ver logs do worker
docker logs dsa-pyspark-cluster-spark-worker-1
```

## 🛠️ Comandos Úteis

### Executar Manualmente no Container
```bash
# Entrar no container
docker exec -it spark-master bash

# Dentro do container, executar o pipeline
spark-submit --master spark://spark-master:7077 /opt/workspace/jobs/etl_pipeline.py
```

### Escalar Workers
```bash
# Aumentar para 3 workers
docker compose up -d --scale spark-worker=3
```

### Limpar Tudo e Recomeçar
```bash
# Para e remove containers
docker compose down

# Remove também volumes e redes
docker compose down -v

# Reinicia do zero
docker compose up -d
```

## ⚠️ Solução de Problemas

### Container não inicia
```bash
# Ver logs completos
docker compose logs

# Reconstruir imagens
docker compose build --no-cache
docker compose up -d
```

### Porta já em uso
Edite o `docker-compose.yml` e altere as portas:
```yaml
ports:
  - "9091:8080"  # Mude 9091 para outra porta disponível
```

### Sem espaço em disco
```bash
# Limpar imagens não utilizadas
docker system prune -a
```

## 📚 Próximos Passos

1. **Adicione seus próprios dados JSON** em `workspace/dados/`
2. **Modifique as transformações** em `workspace/jobs/etl_pipeline.py`
3. **Crie novas agregações** conforme sua necessidade
4. **Integre com bancos de dados** usando as configurações em `config_example.py`

## 💡 Dicas

- Use `simple_example.py` para testar rapidamente modificações
- Logs detalhados aparecem no terminal durante a execução
- Formato Parquet é mais eficiente que CSV para grandes volumes
- Ajuste memória dos workers em `docker-compose.yml` conforme necessário

## 📞 Suporte

Tiago Mars
- GitHub: [@tmarsbr](https://github.com/tmarsbr)
- LinkedIn: [linkedin.com/in/tiago-dados](https://linkedin.com/in/tiago-dados)
- Email: tiagomars233@gmail.com
