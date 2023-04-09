# jagadish-dezoomcamp-final-project
This is Final project by Jagadeesh Dachepalli as part of DataTalksClub DE Zoomcamp 

## Need to run the below steps in the mentioned order to be able create all the required resources for this project in GCP cloud, to deploy and test this project

## Pre-requisites
### VM machine setup
All GCP compute instances  by default comes with `gcloud` SDK in-built
1. add `alias python=python3` in bashrc file
2. `sudo apt-get update`
3. `sudo apt-get install docker.io`
4. To make docker work without sudo
    a. `sudo groupadd docker`
    b. `sudo gpasswd -a $USER docker`
    c. `sudo service docker restart`
5. `sudo apt-get install unzip` and same for wget
6. copy terraform binary inside ~/bin folder(created if bin doesnt exist), unzip and remove the zip file
7. add `export PATH="${HOME}/bin:${PATH}"` at end of ~/.bashrc file

### VM machine - to - GCP setup
0. Have a GCP account and create a project in GCP console
1. Go to `Service Accounts` in the GCP Console, Select the service account and select `manage keys` and Add a key to the service account and and save the automatically downloaded .json file somewhere in a safe location
3. Have the gcloud cli in the system you're planning to test this, store the above json key file in `~/.gc/`
4. add `export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/creds.json` in the bashrc file
5. `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS`

## Terraform
A. Change to `terraform` directory - i.e., run `cd terraform/` 
B. Enable the APIs - billing, artifact, dataproc in the gcp console

1. `terraform init`
2. `terraform apply -var 'project=<project-id-from-gcp>`
3. `terraform output` to validate/check the output values

----
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
2. `docker build -t europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/ipl-2023:v4 .`
3. `docker push europe-west6-docker.pkg.dev/datazoomcamp-jagadish-final/ipl-project/ipl-2023:v4`, once pushed, we can also check the latest version in the gcp console - artifacts service page.
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
### local running with spark-gcloud connection for bigquery and gcp buckets
0. make sure you logged in already using `gcloud auth login`
1. copy the gcloud connector hadoop library from gcloud onto the local directory `gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar lib/gcs-connector-hadoop3-2.2.5.jar` in order for us to be able to load data from files stored in the GCS bucket
2. copy the gcloud connector bigquey library from gcloud to the local directory `gsutil cp gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar lib/spark-bigquery-latest_2.12.jar` in order for us to be able to read/write data from/to BigQuery.
3. convert the jupyter notebook(which we could use for local testing) to a python file using `jupyter nbconvert --to=script generate_stats.ipynb `
4. Edit the python file as per your needs.
5. `cd pyspark_jobs/`
5. now, run the python file `python generate_stats.py`

### DataProc job with DataProc cluster in GCP using terraform
1. for dataproc job, we use the same code but without any jars usage, because it is need only for local runs, they're not needed in GCP environment.
2. we copied the same code another file and removed those jars usage. file name is `generate_stats_dataproc.py`
3. 




## Dashboard
Please remember that this IPL tournament has happened every year from 2008 to 2022 (15 editions so far..).

1. *Dashboard - 1* : This is created using the same data we got from the datalake (ofcourse with a little changes over the raw data, these changes are done in the prefect pipeline before storing the data in Datalake)
    a. This has 2 charts -  1st chart(table) shows number of matches played at each venue and the 2nd 
    chart(pie graph) shows percentages of matches won by batting 1st vs batting 2nd vs matches won in an superover result.
    b. URL - https://lookerstudio.google.com/reporting/5109b6af-c929-4dd2-9f27-be979d92761d/page/io1LD

2. *Dashboard - 2* : This is created using the `team_stats` table which we created and inserted data in the pyspark pipeline using some SQL transformations (union, group by, sort). 
    a. It has 2 pages with 2 different Graphs, please have a look at both of them.
        i. the 1st page has 1 bar graph shows 'total number of matches won' by each team so far in this tournament
        ii. the 2nd page has 1 bar graph again but it shows 'total number of matches palyed vs total number of matches won' by each team so far in this tournament.
    b. URL - https://lookerstudio.google.com/reporting/590f3b48-bdb9-4bf3-924f-e75648bbfe74/page/Sq1LD

3. *Dashboard - 3* : This is created using the `batting_stats` table/data which we created as part of the same pyspark pipeline using SQL transformations(Join, GroupBy, Sum aggregations, sort). 
    a. This dashboard shows 'total number of runs scored' by each batsman for last 10 years (year-wise)
        i. Also, it has some additional feature i.e., a drop-down to select 1 or multiple batsman
        ii. The drop-down shows top 5 run-getters(batsmen).
    b. URL - https://lookerstudio.google.com/reporting/1f70d4c6-ab99-4402-9af5-a2a3bf52c479/page/kl2LD
