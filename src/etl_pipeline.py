'''ETL pipeline to download, process, and load transaction data into Redshift'''
from extract import main as file_downloader
from transform import main as download_and_combine_files
from load import main as upload_data


def run_etl(bucket_name: str) -> None:
    """Run complete ETL process"""
    csv_files = file_downloader(bucket_name)

    output_csv = download_and_combine_files(csv_files)

    upload_data(output_csv)


if __name__ == "__main__":
    BUCKET = 'sigma-resources-truck'
    run_etl(BUCKET)
