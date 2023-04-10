## Prefect cli setup
0. CD to prefect folder `cd ../prefect/`
1. signup at https://www.prefect.io/cloud/ and then login, and create a workspace with name 'ipl-project'
2. `prefect profile create pref_cloud`
3. `prefect profile use pref_cloud`
4. go to `https://app.prefect.cloud/my/api-keys` and create an API key, copy the value
5. `prefect cloud login` and select `paste an API key` and paste the above copied API key value here
6. `prefect cloud workspace set` and select the `ipl-project` workspace



## Testing prefect workflow in Local/Prefect cloud
0. `source ../config/vars`
1. `python blocks/create_gcp_block.py`

for deployment you can choose - 1. plain python file deployment, 2. docker hub docker image deployment Or the 3. GCP cloud run docker image deployment

#### 1st approach - Local testing (optional)
1. `prefect deployment build flows/etl_store_data_to_gcs.py:etl_store_to_gcs -n "deploy ETL job for web to gcs bucket" --cron "*/5 * * * *"`
2. `prefect deployment apply etl_store_to_gcs-deployment.yaml`
3. `prefect agent start -q 'default' ` to start the agent locally
4. Verify the files (`IPL matches` and `IPL ball by ball`) have been created/updated in the GCP storage bucket


#### 2nd approach - build docker file and use docker hub as a repsoitory
0. Chane Directory to PREFECT folder - `cd prefect/`
1. build docker image - `docker build -t 4329/etl_store_to_gcs:ipl-project-new ./`
2. push docker image to docker hub repo - `docker push 4329/etl_store_to_gcs:ipl-project-new`
3. create a prefect block for infrastructure to pull from docker repo - `python blocks/create_docker_block.py`
4. create a deployment from flow and docker-infra prefect block and trigger a deployment `python flows/docker_deploy.py` (make sure you have an agent running to handle this deployment job) - This step will trigger a deployment and will wait for result, and once the agent runs the job it will return status to this call and this code will print that status at the end.
5. somehow, this prefect `run_deployment` is not taking schedule expressions, and 1 github issue says it's a bug, so I've comeup with another approach.
6. now edit that `output.yaml` file `schedule` section to the required schedule we want by giving appropriate cron expressions.
eg: ```schedule:
        cron: 30 16 * * *
        timezone: null
        day_or: true
    ```
8. run `prefect deployment apply ouput.yaml` to apply the schedule which will auto-trigger the jobs, however, even at this point also the agent should run by us locally.


#### 3rd approach - pushing docker image to the GCP artifact repository
0. Chane Directory to PREFECT folder  - `cd prefect/`
1. copy repo path from GCP artifact console eg: `europe-west6-docker.pkg.dev/optimum-attic-383216/ipl-data-analysis`
2. Now use that copied value to build a docker image - `docker build -t europe-west6-docker.pkg.dev/optimum-attic-383216/ipl-data-analysis/ipl-2023:v1 .`

*** Make sure to run this command `gcloud auth configure-docker europe-west6-docker.pkg.dev` to grant access to the GCP artifactory repositories. Change the region incase you're using any different GCP region. ***

3. Push the docker image to the GCP artifactory `docker push europe-west6-docker.pkg.dev/optimum-attic-383216/ipl-data-analysis/ipl-2023:v1`, once pushed, we can also check the latest version in the gcp console - artifacts service page.
4. provide the latest docker image's tag version in the `blocks/create_cloud_run_block.py` file and run `python blocks/create_cloud_run_block.py` 
5. Run `python flows/cloud_run_job_deploy.py` to create a prefect deployment with GCP artifactory cloud run.
6. now edit that yaml file schedule section to the required schedule we want by giving appropriate cron expressions like below for example:
for every 5 minutes
    ```schedule:
        cron: */5 * * * *
        timezone: null
        day_or: true
    ```
8. run `prefect deployment apply cloud-run-job-ouput.yml` to apply the schedule which will auto-trigger the jobs, even at this point also the agent should run by us *locally* . However, the actual flow runs are handled/exeucted by google cloud run jobs.

9. * This gcp cloud run jobs approach gives us the following benefits * :
    i. scalable serverless flows to handle multiple requests/flows along with scalable Memory,CPUs for the jobs/workers.
    ii. setting up is easy, we just need a prefect block for infra code with gcp cloud run infra
    iii. the gcp creds and cloud run infra block needs to be created once but can use many times by multiple flows
    iv. for more info, please refer - https://medium.com/the-prefect-blog/serverless-prefect-flows-with-google-cloud-run-jobs-23edbf371175
