import pandas as pd
import os
from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket, cloud_storage_upload_blob_from_string

from utils import clean_match_data, clean_ball_data

GCP_BUCKET = os.environ['project_name']
GCP_CREDENTIALS = GcpCredentials.load("zoom-gcp-creds")


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read IPL data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)
    print(df.dtypes)
    return df


@task(log_prints=True)
def clean(df, dataset_type: str) -> pd.DataFrame:
    """Fix dtype issues"""

    if dataset_type == "match":
        df = clean_match_data(df)
    elif dataset_type == "ball":
        df = clean_ball_data(df)
    print("data succesfully cleansed")
    print(df.dtypes)
    return df


@task(log_prints=False)
def write_local(df: pd.DataFrame, file_name: str):
    """
        Write DataFrame out locally(in-memory) as parquet file and returns the content in bytes
    """
    content = df.to_parquet(compression="gzip")
    print(type(content))
    return content


@flow()
def etl_store_to_gcs() -> None:
    """The main ETL function: transfers data from external source to the Google Cloud Platform storage bucket"""
    IPL_ball_by_ball_dataset = "https://ipl-data.s3.ap-south-1.amazonaws.com/IPL_Ball_by_Ball_2008_2022.zip"
    IPL_matches_dataset = "https://ipl-data.s3.ap-south-1.amazonaws.com/IPL_Matches_2008_2022.zip"

    data_sources = [
        { 
            "data" : IPL_matches_dataset,
            "type" : "match"
        },
        {
            "data" : IPL_ball_by_ball_dataset,
            "type" : "ball"
        }
    ]

    for source in data_sources:
        df = fetch(source['data'])
        df_clean = clean(df, dataset_type=source['type'])
        file_name = source['data'].split("/")[-1]
        file_name = file_name.replace("zip", "parquet")
        content = write_local(df_clean, file_name)
        
        url = cloud_storage_upload_blob_from_string(content, GCP_BUCKET, file_name, GCP_CREDENTIALS)
        print("file name/url in the GCP storage bucket: ", url)


if __name__ == "__main__":
    etl_store_to_gcs()
