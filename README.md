# jagadish-dezoomcamp-final-project
This is Final project by Jagadeesh Dachepalli as part of DataTalksClub DE Zoomcamp 

## Need to run the below steps in the mentioned order to be able create all this project required resources in GCP cloud and test this project

### Pre-requisites
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

### Terraform
1. `terraform init`
2. `terraform apply`
3. `terraform output` to validate the output values


### venv & prefect cli setup
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


https://ipl-data.s3.ap-south-1.amazonaws.com/IPL_Ball_by_Ball_2008_2022.zip
https://ipl-data.s3.ap-south-1.amazonaws.com/IPL_Matches_2008_2022.zip

### Prefect
0. `source config/vars`
1. `python prefect/blocks/create_gcp_block.py`
#### cli commands
2. `prefect deployment build prefect/flows/etl_store_data_to_gcs.py:etl_store_to_gcs -n "deploy ETL job for web to gcs bucket" --cron "*/5 * * * *"`
3. `prefect deployment apply etl_store_to_gcs-deployment.yaml`
4. `prefect agent start -q 'default'` to start the agent locally
#### build docker file instead of normal python file deployment
0. Chane Directory to PREFECT folder - `cd prefect/`
5. build docker image - `docker build -t 4329/etl_store_to_gcs:ipl-project-new ./`
6. push docker image to docker hub repo - `docker push 4329/etl_store_to_gcs:ipl-project-new`
7. create a prefect block for infrastructure to pull from docker repo - `python blocks/create_docker_block.py`
8. create a deployment from flow and docker-infra prefect block and trigger a deployment `python flows/docker_deploy.py` (make sure you have an agent running to handle this deployment job) - This step will trigger a deployment and will wait for result, and once the agent runs the job it will return status to this call and this code will print that status at the end.





###### not needed as of this commit point
3. `gcloud auth configure-docker europe-west6-docker.pkg.dev`
europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project
4. docker build -t europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/etl_store_to_gcs:final-de-zoomcamp prefect/
5.  docker push europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/etl_store_to_gcs:final-de-zoomcamp
6. 