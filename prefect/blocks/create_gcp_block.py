import os
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

GCP_BUCKET = os.environ.get('gcp_bucket', 'no_bucket_name')

# alternative to creating GCP blocks in the UI
# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

creds_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
content =open(creds_path, "r").read() 

credentials_block = GcpCredentials(
    service_account_info=content # enter your credentials info or use the file method.
    # service_account_file= "~/.gc/finaldatazoomcamp.json" #path to json file
)
credentials_block.save("zoom-gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("zoom-gcp-creds"),
    bucket=GCP_BUCKET,
)

bucket_block.save("zoom-gcs", overwrite=True)
