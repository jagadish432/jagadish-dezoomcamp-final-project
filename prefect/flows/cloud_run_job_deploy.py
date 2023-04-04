from etl_store_data_to_gcs import etl_store_to_gcs
from prefect.deployments import Deployment, run_deployment
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.cloud_run import CloudRunJob


gcs_block = GcsBucket.load("zoom-gcs")
cloud_run_job_block = CloudRunJob.load("zoom-gcp-cloud-run")

DEPLOYMENT_NAME = "fetch-ipl-data-cloud-run-job-deployment"
OUTPUT_YAML_FILE_PATH = "/home/jagadish/jagadish-dezoomcamp-final-project/prefect/cloud-run-job-ouput.yml"


deployment = Deployment.build_from_flow(
    flow=etl_store_to_gcs,
    name=DEPLOYMENT_NAME,
    # storage=gcs_block,
    infrastructure=cloud_run_job_block,
    output=OUTPUT_YAML_FILE_PATH
)

print(deployment)
