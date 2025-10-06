# Dados - Arquivos JSON de Exemplo

Esta pasta contém arquivos JSON de exemplo para demonstrar o pipeline ETL.

## Arquivos Disponíveis

### 1. usuarios_api.json
Dados simulados de usuários obtidos de uma API.

**Estrutura:**
```json
{
  "id": integer,
  "nome": string,
  "email": string,
  "idade": integer (pode ser null),
  "cidade": string,
  "data_cadastro": timestamp,
  "ativo": boolean,
  "tags": array<string>
}
```

**Características:**
- 5 registros de exemplo
- Demonstra dados faltantes (null)
- Inclui arrays (tags)
- Representa dados típicos de CRM

### 2. transacoes_api.json
Dados simulados de transações financeiras.

**Estrutura:**
```json
{
  "transacao_id": string,
  "usuario_id": integer,
  "valor": float,
  "moeda": string,
  "data_transacao": timestamp,
  "status": string,
  "metodo_pagamento": {
    "tipo": string,
    "bandeira": string (opcional),
    "ultimos_digitos": string (opcional),
    "chave": string (opcional)
  }
}
```

**Características:**
- 5 registros de exemplo
- Demonstra JSON aninhado (metodo_pagamento)
- Diferentes métodos de pagamento
- Estados de transação variados

### 3. sensores_iot.json
Leituras simuladas de sensores IoT.

**Estrutura:**
```json
{
  "sensor_id": string,
  "tipo": string,
  "localizacao": {
    "sala": string,
    "andar": integer,
    "predio": string
  },
  "leitura": float,
  "unidade": string,
  "timestamp": timestamp,
  "status": string
}
```

**Características:**
- 5 registros de exemplo
- Demonstra dados de séries temporais
- JSON aninhado (localizacao)
- Múltiplas leituras do mesmo sensor

## Como Adicionar Seus Próprios Dados

1. Coloque seus arquivos JSON nesta pasta
2. Ajuste os scripts em `../jobs/` para processar seus arquivos
3. Certifique-se de que seus JSONs sejam válidos

**Dica:** Use ferramentas como [JSONLint](https://jsonlint.com/) para validar seus arquivos JSON.

## Formato dos Arquivos

Todos os arquivos usam formato JSON com múltiplas linhas (multiLine=true no Spark):
```json
[
  {
    "campo1": "valor1",
    "campo2": "valor2"
  },
  {
    "campo1": "valor3",
    "campo2": "valor4"
  }
]
```

## Casos de Uso Representados

- **usuarios_api.json**: Integração com APIs de terceiros
- **transacoes_api.json**: Processamento de eventos financeiros
- **sensores_iot.json**: Telemetria e monitoramento em tempo real
