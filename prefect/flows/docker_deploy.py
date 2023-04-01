from prefect.deployments import Deployment, run_deployment
from etl_store_data_to_gcs import etl_store_to_gcs
from prefect.infrastructure.docker import DockerContainer


docker_container_block = DockerContainer.load("zoom-docker")

DEPLOYMENT_NAME = "fetch-ipl-data-docker-deployment"

docker_dep = Deployment.build_from_flow(
    flow=etl_store_to_gcs,
    name=DEPLOYMENT_NAME,
    infrastructure=docker_container_block,
    apply=True
)

print(docker_dep)

def create_schedule():
    response = run_deployment(
        name=f"{docker_dep.flow_name}/{docker_dep.name}",
        # scheduled_time="*/5 * * * *",
        flow_run_name="fetch-ipl-data-docker-scheduler"
    )
    return response


if __name__ == "__main__":
    print(create_schedule())
    # print(None)
