# -*- coding: utf-8 -*-
"""
Google Cloud Function para carregar dados de arquivos CSV do GCS para o BigQuery
automaticamente quando um arquivo é adicionado/modificado no bucket.
"""

from google.cloud import bigquery
import os


GCP_PROJECT_ID = "projeto-case-459220"  
BIGQUERY_DATASET_ID = "Case"          


FILE_TO_TABLE_MAPPING = {
    "Caixin_PMI.csv": {
        "table_id": "caixin_pmi_cny", # Nome da tabela no BigQuery
        "schema": [
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("actual_state", "FLOAT"),
            bigquery.SchemaField("close", "FLOAT"),
            bigquery.SchemaField("forecast", "FLOAT"),
        ]
    },
    "USD_CNY.csv": {
        "table_id": "usd_cny", # Nome da tabela no BigQuery
        "schema": [
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("close", "FLOAT"),
            bigquery.SchemaField("open", "FLOAT"),
            bigquery.SchemaField("high", "FLOAT"),
            bigquery.SchemaField("low", "FLOAT"),
            bigquery.SchemaField("volume", "FLOAT"),
        ]
    },
    "ism_services_pmi_full_eua.csv": {
        "table_id": "ism_pmi_eua", # Nome da tabela no BigQuery
        "schema": [
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("actual_state", "FLOAT"),
            bigquery.SchemaField("close", "FLOAT"),
            bigquery.SchemaField("forecast", "FLOAT"),
        ]
    }
}

def gcs_to_bq_loader(event, context):
    """Função Cloud acionada por um evento do GCS (upload/modificação de arquivo).

    """
    file_name = event["name"]
    bucket_name = event["bucket"]
    gcs_uri = f"gs://{bucket_name}/{file_name}"

    print(f"Evento recebido para o arquivo: {file_name} no bucket: {bucket_name}")
    print(f"Context ID: {context.event_id}")
    print(f"Context Timestamp: {context.timestamp}")

    # Verifica se o arquivo está no mapeamento
    if file_name not in FILE_TO_TABLE_MAPPING:
        print(f"Arquivo {file_name} não está no mapeamento. Ignorando.")
        return

    table_config = FILE_TO_TABLE_MAPPING[file_name]
    table_id = table_config["table_id"]
    schema = table_config["schema"]

    print(f"Processando arquivo: {file_name}")
    print(f"Carregando para a tabela: {GCP_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{table_id}")

    client = bigquery.Client(project=GCP_PROJECT_ID)
    table_ref = client.dataset(BIGQUERY_DATASET_ID).table(table_id)

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Pular a linha de cabeçalho no CSV
        autodetect=False,     # Usar o schema definido
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Substitui a tabela se ela existir
    )

    try:
        load_job = client.load_table_from_uri(
            gcs_uri,
            table_ref,
            job_config=job_config
        )
        print(f"Iniciando job de carga {load_job.job_id} para {gcs_uri}")

        load_job.result()  # Espera o job ser concluído.

        destination_table = client.get_table(table_ref)
        print(f"Job {load_job.job_id} concluído. Carregadas {destination_table.num_rows} linhas em {GCP_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{table_id}.")
    except Exception as e:
        print(f"Erro ao carregar dados de {gcs_uri} para {GCP_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{table_id}: {e}")
        # Considerar levantar a exceção para que o GCP possa registrar a falha e tentar novamente se configurado.
        raise

# Exemplo de como o evento do GCS se parece (para referência):
# event = {
#     "bucket": "seu-bucket-de-dados",
#     "name": "Caixin_PMI.csv",
#     "metageneration": "1",
#     "timeCreated": "2020-04-23T07:38:57.230Z",
#     "updated": "2020-04-23T07:38:57.230Z"
# }
# context = None 

# Para testar localmente (simulando um evento), você pode descomentar e adaptar:
# if __name__ == "__main__":
#     # Simula um evento para o arquivo Caixin_PMI.csv
#     simulated_event_caixin = {
#         "bucket": "dados-case", # Use o nome do seu bucket real
#         "name": "Caixin_PMI.csv"
#     }
#     # Simula um evento para o arquivo USD_CNY.csv
#     simulated_event_usd_cny = {
#         "bucket": "dados-case", # Use o nome do seu bucket real
#         "name": "USD_CNY.csv"
#     }
#     class MockContext:
#         event_id = "test-event-id"
#         timestamp = "test-timestamp"
#     mock_context = MockContext()
#     print("--- Testando com Caixin_PMI.csv ---")
#     gcs_to_bq_loader(simulated_event_caixin, mock_context)
#     print("\n--- Testando com USD_CNY.csv ---")
#     gcs_to_bq_loader(simulated_event_usd_cny, mock_context)