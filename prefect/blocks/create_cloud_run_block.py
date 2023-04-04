import os
from prefect_gcp.cloud_run import CloudRunJob
from prefect_gcp import GcpCredentials


gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")


# alternatively, we can also create this block in the prefect cloud UI manually
cloud_run_block = CloudRunJob(
    image="europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/ipl-2023:v3",  # insert your docker artifact image uri here
    region=os.environ['region'],
    cpu=1,
    memory=512,
    memory_unit='Mi',
    credentials=gcp_credentials_block
)

cloud_run_block.save("zoom-gcp-cloud-run", overwrite=True)
