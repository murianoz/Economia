# 📊 Case de Engenharia de Dados: Pipeline de Dados Econômicos com GCP

## 🎯 Objetivo

Desenvolver um pipeline para coletar, processar e armazenar dados econômicos públicos, visando subsidiar análises preditivas sobre o preço do papel, utilizando serviços do Google Cloud Platform (GCP).

## 📁 Dados Utilizados

- 🇨🇳 **Caixin PMI China** – Fonte: mql5  
- 💵 **USD/CNY** – Fonte: yfinance  
- 🇺🇸 **ISM PMI EUA** – Fonte: investing  
- 🧾 Arquivos CSV gerados:  
  `Caixin_PMI.csv`, `USD_CNY.csv`, `ism_services_pmi_full_eua.csv`

## 🏗️ Arquitetura

-  **Google Cloud Storage (GCS)**: Armazena os arquivos CSV.  
-  **Google BigQuery**: Armazena e consulta os dados estruturados.  
-  **Google Cloud Functions**: Automatiza a carga de dados do GCS para o BigQuery.  
-  **Scripts Python**:
  - `Indice_pmi.py`:  Coleta e trata dados do Caixin PMI China.
  - `usd_cny.py`:  Coleta e trata dados da cotação USD/CNY.
  - `pmi_eua.py`:  Coleta e trata dados do ISM PMI EUA.
  - `2_registros.py`:  Exibe número de registros extraídos.
  - `main.py`:  Função para Cloud Functions.
  - `Pipeline.py`:  Lê CSVs e carrega no BigQuery.
  - `Deploy.cmd`:  Script de deploy da Cloud Function.

## 🚀 Execução

1. **Executar os scripts de coleta e tratamento dos dados:**
   ```bash
   python Indice_pmi.py
   python usd_cny.py
   python pmi_eua.py
   ```

2. **📤 Subir os arquivos CSV para o bucket GCS (ex: `dados-case`)**

3. **🗂️ Criar um dataset no BigQuery (ex: `economia`)**

4. **⚙️ Atualizar as variáveis nos scripts:**
   - `GCP_PROJECT_ID`
   - `BIGQUERY_DATASET_ID`
   - `GCS_BUCKET_NAME`

5. **📡 Carregar os dados no BigQuery**:
   - **🔧 Manualmente (executar localmente):**
     ```bash
     python Pipeline.py
     ```
   - **🤖 Automatizado (via Cloud Functions):**
     - Executar `Deploy.cmd` para subir `main.py`
     - A função será acionada automaticamente quando um novo CSV for enviado ao GCS.

## 🗃️ Estrutura das Tabelas

- `caixin_pmi_china`: `date`, `actual_state`, `close`, `forecast`
- `usd_cny_daily`: `date`, `close`, `open`, `high`, `low`, `volume`
- `ism_pmi_usa`: `date`, `actual`

## ⛓️ Orquestração

- **Cloud Functions**: disparada automaticamente ao receber arquivos no GCS.

## 📄 A query SQL utilizada para agregação mensal encontra-se também no arquivo cloud.sql
---

ℹ️ Observações
A biblioteca investpy não foi utilizada neste projeto, pois está descontinuada e não é mais mantida pela comunidade.

Em vez disso, os dados foram coletados manualmente ou com auxílio de outras bibliotecas como yfinance ou via scraping direto dos sites.

 **Este projeto foi construído com foco em simplicidade, escalabilidade e uso eficiente dos recursos gratuitos do GCP.**
