'''Clean data and combine into a CSV'''
import os
import pandas as pd
from extract_data import main as file_downloader


def clean_data(transaction_data):
    """Cleans the transaction data by removing rows with invalid totals and converting data types"""

    cleaned_data = transaction_data.copy()

    cleaned_data = cleaned_data.loc[cleaned_data['total'].notna()]

    cleaned_data['total_str'] = cleaned_data['total'].astype(str)
    cleaned_data = cleaned_data.loc[cleaned_data['total_str'].str.lower(
    ) != 'void']

    cleaned_data['total'] = pd.to_numeric(
        cleaned_data['total'], errors='coerce')
    cleaned_data = cleaned_data.loc[(
        cleaned_data['total'] > 0) & (cleaned_data['total'] < 100)]

    cleaned_data['timestamp'] = pd.to_datetime(
        cleaned_data['timestamp'], errors='coerce')
    cleaned_data = cleaned_data.dropna(subset=['timestamp', 'total'])

    cleaned_data = cleaned_data.drop(columns=['total_str'])

    return cleaned_data


def combine_transaction_data_files(transaction_files, combined_output_path):
    """Combines transaction files from the data/ folder.
    Produces a single combined CSV file in the data/ folder, then deletes the individual files
    """

    all_transactions = []

    for file in transaction_files:
        file_path = os.path.join('../data', file)
        transaction_data = pd.read_csv(file_path)

        truck_id = file.split('_')[1][1:]
        transaction_data['truck_id'] = truck_id

        cleaned_transaction_data = clean_data(transaction_data)

        all_transactions.append(cleaned_transaction_data)

        os.remove(file_path)

    combined_transaction_data = pd.concat(all_transactions, ignore_index=True)

    combined_transaction_data.to_csv(combined_output_path, index=False)
    print(f"Combined transaction data saved to {combined_output_path}")


def main(bucket_name: str) -> str:
    """Download files from bucket and combine into a single CSV file"""
    csv_files = file_downloader(bucket_name)
    output_csv = '../data/' + \
        '/'.join(csv_files[0].split('/')[:-1]) + '/combined_data.csv'
    combine_transaction_data_files(csv_files, output_csv)
    return output_csv


if __name__ == "__main__":
    BUCKET = 'sigma-resources-truck'
    main(BUCKET)
