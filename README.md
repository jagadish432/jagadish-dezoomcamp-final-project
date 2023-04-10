# jagadish-dezoomcamp-final-project
This is Final project by Jagadeesh Dachepalli as part of DataTalksClub DE Zoomcamp 

### Need to run the below steps in the mentioned order to be able create all the required resources for this project in GCP cloud, to deploy and test this project

## Pre-requisites
We need to setup the system, incase we're planning to test this project. 
Please refer the file [setup.md](./setup.md) for more details.


## Terraform
We need to create some infrastructure over a cloud(in this case I'm using Google Cloud), so we're using `terraform` for IaC(Infrastructure as Code) to deploy the resources in an efficient manner.
Please refer the file [terraform.md](./terraform.md) for more details.


## venv setup
0. Run `sudo apt-get install python3-venv` to install python virtual environment package
1. Create a python virtual enviornment - `python -m venv ipl_venv`
2. Activate the virtual environemnt `source ipl_venv/bin/activate`
3. Install all required python packages in the virtual environment - `pip install -r prefect/requirements.txt`
4. Check the prefect version - `prefect --version`


## Prefect setup and test
Please refer this [prefect.md file](./prefect.md) for more information.








## Spark pipeline

### local running with spark-gcloud connection for bigquery and gcp buckets(optional)
0. make sure you logged in already using `gcloud auth login`
1. copy the gcloud connector hadoop library from gcloud onto the local directory `gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar lib/gcs-connector-hadoop3-2.2.5.jar` in order for us to be able to load data from files stored in the GCS bucket
2. copy the gcloud connector bigquey library from gcloud to the local directory `gsutil cp gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar lib/spark-bigquery-latest_2.12.jar` in order for us to be able to read/write data from/to BigQuery.
3. convert the jupyter notebook(which we could use for local testing) to a python file using `jupyter nbconvert --to=script generate_stats.ipynb `
4. Edit the python file as per your needs.
5. `cd pyspark_jobs/`
5. now, run the python file `python generate_stats.py`

### DataProc job with DataProc cluster in GCP using python file
A. CD to `pyspark_jobs` folder
1. change the gcp project name in the file `generate_stats_dataproc.py`
2. now run `gsutil cp generate_stats_dataproc.py gs://jagadish_data_lake_optimum-attic-383216/generate_stats_dataproc.py`
3. but we run trigger a dataproc job using another python file. run `python submit_dataproc_job.py`



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
