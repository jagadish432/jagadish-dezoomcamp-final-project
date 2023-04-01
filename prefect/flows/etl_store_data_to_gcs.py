from pathlib import Path
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket, cloud_storage_upload_blob_from_string


GCP_BUCKET = os.environ['gcp_bucket']


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
    # df['City'] = df['City'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'])

    df['Season'] = df['Season'].apply(fix_season_value)
    df['Season'] = df['Season'].astype(int)

    # df['Team1'] = df['Team1'].astype(str)
    # df['Team2'] = df['Team2'].astype(str)
    # df['Venue'] = df['Venue'].astype(str)
    # df['TossWinner'] = df['TossWinner'].astype(str)
    # df['TossDecision'] = df['TossDecision'].astype(str)
    # df['SuperOver'] = df['SuperOver'].astype(str)
    # df['WinningTeam'] = df['WinningTeam'].astype(str)
    # df['WonBy'] = df['WonBy'].astype(str)

    df["Margin"].fillna(-1, inplace=True)
    df['Margin'] = df['Margin'].astype(int)

    # df['method'] = df['method'].astype(str)
    # df['Player_of_Match'] = df['Player_of_Match'].astype(str)
    # df['Umpire1'] = df['Umpire1'].astype(str)
    # df['Umpire2'] = df['Umpire2'].astype(str)
    # df['Team1Players'] = df['Team1Players'].astype(str)
    # df['Team2Players'] = df['Team2Players'].astype(str)

    df['Team1Players'] = df['Team1Players'].str.split(",")
    df['Team2Players'] = df['Team2Players'].str.split(",")

    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, file_name: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{file_name}")
    content = df.to_parquet(compression="gzip")
    print(type(content))
    return content


@task()
def write_gcs(path: Path, content) -> None:
    """Upload local parquet file to GCS"""
    # gcs_block = GcsBucket.load("zoom-gcs")
    gcp_credentials = GcpCredentials.load("zoom-gcp-creds")
    blob = cloud_storage_upload_blob_from_string(
        content, GCP_BUCKET, path, gcp_credentials)
    return blob


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
        # file_url = write_gcs(file_name, content)
        gcp_credentials = GcpCredentials.load("zoom-gcp-creds")
        blob = cloud_storage_upload_blob_from_string(
            content, GCP_BUCKET, file_name, gcp_credentials)
        print("file name/url: ", blob)


if __name__ == "__main__":
    etl_store_to_gcs()
