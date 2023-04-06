# jagadish-dezoomcamp-final-project
This is Final project by Jagadeesh Dachepalli as part of DataTalksClub DE Zoomcamp 

## Need to run the below steps in the mentioned order to be able create all this project required resources in GCP cloud and test this project

## Pre-requisites
1. make sure you have a gcp service account, go to `https://console.cloud.google.com/iam-admin/serviceaccounts?project=<gcp-project-name>` in this case `https://console.cloud.google.com/iam-admin/serviceaccounts?project=datazoomcamp-jagadish-final` 
2. select the service account and select `manage keys`
3. select `Add key` and `JSON` and save the automatically downloaded .json file somewhere in a safe location
4. `gcloud auth login`, click on the link, allow access, copy the code and paste in the terminal prompting for the authorization code
5. verify if the project is already set with your required project `gcloud config get project`
6. if not, then `gcloud config set project <gcp-project-name>`
7. To set the gcloud automatically access the required project, follow either of the below approaches
    a. REFRESH TOKEN approach
        1. run `gcloud auth application-default login` and enter Y when prompted, click on the link provided and login to the gcp console and copy the authorization code and paste in the terminal where prompted
        2. verify `~/.config/gcloud/application_default_credentials.json` it has the updated and the required project creds now
        3. `unset GOOGLE_APPLICATION_CREDENTIALS`
    b. To use the download gcp creds file directly(json file)
        1. cd to `~/.gc/`
        2. create a json file and copy the content
        3. now set the env variable `export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/<json file_name>`
        4. keep the above export command in your bash profile file to make it permanent env variable i.e., you wouldn't need to set everytime you open a terminal

## Terraform
1. `terraform init`
2. `terraform apply`
3. `terraform output` to validate the output values


## venv & prefect cli setup
0. signup at https://www.prefect.io/cloud/ and then login, and create a workspace with name 'ipl-project'
1. `python -m venv ipl_venv`
2. `source ipl_venv/bin/activate`
3. `pip install -r prefect/requirements.txt`
4. `prefect --version`
5. `prefect profile create pref_cloud`
6. `prefect profile user pref_cloud`
7. go to `https://app.prefect.cloud/my/api-keys` and create an API key, copy the value
8. `prefect cloud login` and select `paste an API key` and paste the above copied API key value here
9. `prefect cloud workspace set` and select the `ipl-project` workspace


## Prefect
0. `source config/vars`
1. `python prefect/blocks/create_gcp_block.py`
### cli commands
2. `prefect deployment build prefect/flows/etl_store_data_to_gcs.py:etl_store_to_gcs -n "deploy ETL job for web to gcs bucket" --cron "*/5 * * * *"`
3. `prefect deployment apply etl_store_to_gcs-deployment.yaml`
4. `prefect agent start -q 'default'` to start the agent locally
### build docker file instead of normal python file deployment
0. Chane Directory to PREFECT folder - `cd prefect/`
5. build docker image - `docker build -t 4329/etl_store_to_gcs:ipl-project-new ./`
6. push docker image to docker hub repo - `docker push 4329/etl_store_to_gcs:ipl-project-new`
7. create a prefect block for infrastructure to pull from docker repo - `python blocks/create_docker_block.py`
8. create a deployment from flow and docker-infra prefect block and trigger a deployment `python flows/docker_deploy.py` (make sure you have an agent running to handle this deployment job) - This step will trigger a deployment and will wait for result, and once the agent runs the job it will return status to this call and this code will print that status at the end.
9. somehow, this prefect `run_deployment` is not taking schedule expressions, and 1 github issue says it's a bug, so I've comeup with another approach.

### DIFF APPROACH - still with dockerhub docker file
10. we will still follow the above points - 5,6,7,8 (but the file in 8th step has a little changes that it won't trigger any job and now it'll create an output.yaml file in the local)
11. now edit that yaml file schedule section to the required schedule we want by giving appropriate cron expressions.
12. run `prefect deployment apply ouput.yaml` to apply the schedule which will auto-trigger the jobs, however, even at this point also the agent should run by us locally.

### pushing docker image to the GCP artifact repository
0. `cd prefect/`
1. copy repo path from GCP artifact console - `europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project`.
2. `docker build -t europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/ipl-2023:v2 .`
3. `docker push europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/ipl-2023:v2`, once pushed, we can also check the latest version in the gcp console - artifacts service page.
4. provide the proper docker image's tag version in the `blocks/create_cloud_run_block.py` file and run `python blocks/create_cloud_run_block.py` 
5.  and `python flows/cloud_run_job_deploy.py`
6. now edit that yaml file schedule section to the required schedule we want by giving appropriate cron expressions like below for example:
    ```schedule:
        cron: 30 16 * * *
        timezone: null
        day_or: true
    ```
7. enable `cloud run API` in the GCP console.
8. run `prefect deployment apply cloud-run-job-ouput.yml` to apply the schedule which will auto-trigger the jobs, even at this point also the agent should run by us *locally* . However, the actual flow runs are handled/exeucted by google cloud run jobs.

9. *This gcp cloud run jobs approach gives us the following benefits* :
    a. scalable serverless flows to handle multiple requests/flows
    b. setting up is easy, we just need a prefect block for infra code with gcp cloud run infra
    c. the gcp creds and cloud run infra block needs to be created once but can use many times by multiple flows
    d. for more info, please refer - https://medium.com/the-prefect-blog/serverless-prefect-flows-with-google-cloud-run-jobs-23edbf371175


## Spark pipeline
### local running
### spark-gcloud connection
0. make sure you logged in already using `gcloud auth login`
1. copy the gcloud connector hadoop library from gcloud onto the local directory `gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar lib/gcs-connector-hadoop3-2.2.5.jar` in order for us to be able to load data from files stored in the GCS bucket
2. copy the gcloud connector bigquey library from gcloud to the local directory `gsutil cp gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar lib/spark-bigquery-latest_2.12.jar` in order for us to be able to read/write data from/to BigQuery.

#### TODO
1. write a local pyspark job to read gcs parquet files
2. comeup with the join conditions needed for matches and balls data to bring batting/bowling/team statistics
3. save them to the bigquery table
4. create a dataproc cluster using terraform
5. execute the 1,2,3 points using dataproc spark job


## Dashboard
1. create a google studio dashboard and fetch data from bigquery facts table created in the `Spark pipeline` step.

