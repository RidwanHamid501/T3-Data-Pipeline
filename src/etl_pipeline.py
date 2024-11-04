'''ETL pipeline to download, process, and load transaction data into Redshift'''
from transform_data import main as download_and_combine_files
from load_data import main as upload_data


def run_etl(bucket_name: str) -> None:
    """Run complete ETL process"""
    output_csv = download_and_combine_files(bucket_name)

    upload_data(output_csv)


if __name__ == "__main__":
    BUCKET = 'sigma-resources-truck'
    run_etl(BUCKET)
