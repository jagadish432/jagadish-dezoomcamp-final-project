from pathlib import Path
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket, cloud_storage_upload_blob_from_string


GCP_BUCKET = os.environ['gcp_bucket']
GCP_CREDENTIALS = GcpCredentials.load("zoom-gcp-creds")


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read IPL data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)
    print(df.head())
    print(df.dtypes)
    return df


def fix_season_value(season):
    years = season.split("/")
    return years[0]

@task(log_prints=True)
def clean(df=pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    # These columns doesn't need to be converted as they're already of String type: Team1, Team2, Venue, TossWinner, TossDecision, SuperOver, WinningTeam, WonBy,
    # method. Player_of_Match, Umpire1, Umpire2, Team1Players, Team2Players

    # Converting date values to date time
    df['Date'] = pd.to_datetime(df['Date'])

    # fixing 'Season' values, few values have 2008/09 so we're converting them to the 2008
    df['Season'] = df['Season'].apply(fix_season_value)
    df['Season'] = df['Season'].astype(int)

    # Filling/Replacing the superover decided matches Margin(existing as NA) with -1
    df["Margin"].fillna(-1, inplace=True)
    df['Margin'] = df['Margin'].astype(int)

    df['Team1Players'] = df['Team1Players'].str.split(",")
    df['Team2Players'] = df['Team2Players'].str.split(",")

    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
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
    # IPL_ball_by_ball_dataset = "https://ipl-data.s3.ap-south-1.amazonaws.com/IPL_Ball_by_Ball_2008_2022.zip"
    IPL_matches_dataset = "https://ipl-data.s3.ap-south-1.amazonaws.com/IPL_Matches_2008_2022.zip"

    data_sources = [IPL_matches_dataset, ]

    for source in data_sources:
        df = fetch(source)
        df_clean = clean(df)
        file_name = source.split("/")[-1]
        file_name = file_name.replace("zip", "parquet")
        content = write_local(df_clean, file_name)
        
        url = cloud_storage_upload_blob_from_string(
            content, GCP_BUCKET, file_name, GCP_CREDENTIALS)
        print("file name/url in the GCP storage bucket: ", url)


if __name__ == "__main__":
    etl_store_to_gcs()
