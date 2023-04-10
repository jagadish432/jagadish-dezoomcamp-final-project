
### local running with spark-gcloud connection for bigquery and gcp buckets(optional)
0. make sure you logged in already using `gcloud auth login`
1. copy the gcloud connector hadoop library from gcloud onto the local directory `gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar lib/gcs-connector-hadoop3-2.2.5.jar` in order for us to be able to load data from files stored in the GCS bucket
2. copy the gcloud connector bigquey library from gcloud to the local directory `gsutil cp gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar lib/spark-bigquery-latest_2.12.jar` in order for us to be able to read/write data from/to BigQuery.
3. convert the jupyter notebook(which we could use for local testing) to a python file using `jupyter nbconvert --to=script generate_stats.ipynb `
4. Edit the python file as per your needs.
5. `cd pyspark_jobs/`
5. now, run the python file `python generate_stats.py`

### DataProc job with DataProc cluster in GCP using python file
0. CD to `pyspark_jobs` folder
1. but we run trigger a dataproc job using another python file. run `python submit_dataproc_job.py`