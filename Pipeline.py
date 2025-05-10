from google.cloud import bigquery

def load_csv_to_bigquery(project_id, dataset_id, table_id, gcs_uri, schema):
    """Carrega um arquivo CSV do GCS para uma tabela do BigQuery.
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  
        autodetect=False, 
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, 
    )

    try:
        load_job = client.load_table_from_uri(
            gcs_uri,
            table_ref,
            job_config=job_config
        )
        print(f"Iniciando job {load_job.job_id} para carregar {gcs_uri} em {project_id}.{dataset_id}.{table_id}")

        load_job.result()  # Espera o job ser concluído.

        destination_table = client.get_table(table_ref)
        print(f"Job concluído. Carregadas {destination_table.num_rows} linhas em {project_id}.{dataset_id}.{table_id}.")
    except Exception as e:
        print(f"Erro ao carregar dados para {project_id}.{dataset_id}.{table_id}: {e}")

if __name__ == "__main__":

    # --- Configurações do Usuário --- #
    
    GCP_PROJECT_ID = "projeto-case-459220"  
    BIGQUERY_DATASET_ID = "Case" 
    GCS_BUCKET_NAME = "dados-case" 

    tables_to_load = [
        {
            "table_id": "caixin_pmi_cny",
            "gcs_file_name": "Caixin_PMI.csv",
            "schema": [
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("actual_state", "FLOAT"),
                bigquery.SchemaField("close", "FLOAT"),
                bigquery.SchemaField("forecast", "FLOAT"),

            ]
        },
        {
            "table_id": "usd_cny",
            "gcs_file_name": "USD_CNY.csv",
            "schema": [
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("close", "FLOAT"),
                bigquery.SchemaField("open", "FLOAT"),
                bigquery.SchemaField("high", "FLOAT"),
                bigquery.SchemaField("low", "FLOAT"),
                bigquery.SchemaField("volume", "FLOAT"), 
            ]
        },
        {
            "table_id": "ism_pmi_eua",
            "gcs_file_name": "ism_services_pmi_full_eua.csv",
            "schema": [
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("actual_state", "FLOAT"),
                bigquery.SchemaField("close", "FLOAT"),
                bigquery.SchemaField("forecast", "FLOAT"),
            ]
        }
    ]

    print("Iniciando processo de carga de dados para o BigQuery...")
    print(f"AVISO: Certifique-se de que o dataset '{BIGQUERY_DATASET_ID}' existe no projeto '{GCP_PROJECT_ID}'.")
    print(f"Os arquivos CSV devem estar no bucket GCS: 'gs://{GCS_BUCKET_NAME}/'\n")

    for table_info in tables_to_load:
        gcs_uri = f"gs://{GCS_BUCKET_NAME}/{table_info['gcs_file_name']}"
        print(f"\nProcessando tabela: {table_info['table_id']}")
        load_csv_to_bigquery(
            project_id=GCP_PROJECT_ID,
            dataset_id=BIGQUERY_DATASET_ID,
            table_id=table_info['table_id'],
            gcs_uri=gcs_uri,
            schema=table_info['schema']
        )

    print("\nProcesso de carga de dados concluído.")

