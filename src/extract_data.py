"""Download specified truck data files from S3 
uploaded within the last 3 hours into a local folder"""
import os
from datetime import datetime, timedelta
import boto3

HOURS_BEFORE = 3


def get_aws_session() -> boto3.Session:
    """Create and return AWS session"""
    return boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )


def get_files_in_bucket(client: boto3.client, bucket_name: str) -> list[dict]:
    """Fetch all file objects in the specified S3 bucket"""
    bucket_objects = client.list_objects_v2(Bucket=bucket_name)
    return bucket_objects.get('Contents', [])


def generate_time_paths(start_time: datetime, end_time: datetime) -> list[str]:
    """Create a list of hourly path strings from start to end time"""
    time_paths = []
    while start_time <= end_time:
        time_paths.append(start_time.strftime("trucks/%Y-%m/%-d/%H"))
        start_time += timedelta(hours=1)
    return time_paths


def download_files(client: boto3.client, bucket_name: str,
                   files: list[dict], valid_paths: list[str]) -> list[str]:
    """Download matching files from S3 to 'data/' directory if path is valid"""
    downloaded_files = []

    for file_info in files:
        file_key = file_info['Key']
        if any(file_key.startswith(path) for path in valid_paths):
            local_path = os.path.join('../data', file_key)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            client.download_file(bucket_name, file_key, local_path)
            if file_key.endswith('.csv'):
                downloaded_files.append(file_key)

    return downloaded_files


def main(bucket_name: str) -> list[str]:
    """Run the file download process for a specified S3 bucket"""
    session = get_aws_session()
    client = session.client('s3')

    bucket_files = get_files_in_bucket(client, bucket_name)

    cutoff_time = datetime.now() - timedelta(hours=HOURS_BEFORE-1)
    valid_paths = generate_time_paths(cutoff_time, datetime.now())

    downloaded_files = download_files(
        client, bucket_name, bucket_files, valid_paths)

    return downloaded_files


if __name__ == "__main__":
    BUCKET = ''
    main(BUCKET)
