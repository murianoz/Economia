gcloud functions deploy gcs-bq-loader-case --project projeto-case-459220 --region us-central1 --runtime python310 --trigger-resource dados-case --trigger-event google.storage.object.finalize --entry-point gcs_to_bq_loader --source . --service-account cloud-function@projeto-case-459220.iam.gserviceaccount.com --allow-unauthenticated



::.bash
::gcloud functions deploy gcs-bq-loader-case \
::    --project projeto-case-459220 \
::    --region us-central1 \
::    --runtime python310 \
::    --trigger-resource dados-case \
::    --trigger-event google.storage.object.finalize \
::    --entry-point gcs_to_bq_loader \
::    --source . \
::    --service-account SEU_SERVICE_ACCOUNT@projeto-case-459220.iam.gserviceaccount.com \
::    --allow-unauthenticated
