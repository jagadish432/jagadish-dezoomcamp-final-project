from prefect.deployments import Deployment
from etl_store_data_to_gcs import etl_store_to_gcs
from prefect.infrastructure.docker import DockerContainer


docker_container_block = DockerContainer.load("zoom-docker")

docker_dep = Deployment.build_from_flow(
    flow=etl_store_to_gcs,
    name="docker-flow",
    infrastructure=docker_container_block
)


if __name__ == "__main__":
    docker_dep.apply()
