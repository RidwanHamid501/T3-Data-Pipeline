'''Load transaction data into Redshift database'''
from os import environ
import redshift_connector as rc
from dotenv import load_dotenv


def set_search_path(conn: rc.Connection, cursor: rc.Cursor) -> None:
    """Set search path for the database schema"""
    cursor.execute(f"SET search_path TO {environ['SCHEMA']}")
    conn.commit()


def get_connection() -> rc.Connection:
    '''Retrieve redshift connection'''
    return rc.connect(
        host=environ["HOST"],
        port=environ["PORT"],
        database=environ["DATABASE_NAME"],
        user=environ["USERNAME"],
        password=environ["PASSWORD"]
    )


def get_payment_method_id(payment_method: str, cursor: rc.Cursor) -> int:
    """Return ID of payment method"""
    get_id_query = "SELECT payment_method_id FROM DIM_Payment_Method WHERE payment_method = %s"
    cursor.execute(get_id_query, (payment_method,))
    result = cursor.fetchone()
    if result:
        return result[0]
    raise ValueError(f"""Payment method '{
        payment_method}' not found in database""")


def upload_transaction_data(conn: rc.Connection, cursor: rc.Cursor,
                            transaction_records: list[str]) -> None:
    """Upload transaction data to the FACT_Transaction table using batch processing"""

    insert_query = """
    INSERT INTO FACT_Transaction (truck_id, payment_method_id, total, at)
    VALUES (%s, %s, %s, %s)
    """

    batch_data = []
    for row in transaction_records:
        truck_id = row[3]
        payment_method_id = row[1]
        total = row[2]
        timestamp = row[0]

        row = row.split(',')
        payment_id = get_payment_method_id(payment_method_id, cursor)
        batch_data.append((truck_id, payment_id, total, timestamp))

    cursor.executemany(insert_query, batch_data)
    conn.commit()


def load_csv(combined_data_file: str) -> list[str]:
    """Load and return contents of the CSV file as a list of rows"""
    with open(combined_data_file, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def main(file_path: str) -> None:
    """Main function to load data from the CSV file into the database"""
    load_dotenv()
    connection = get_connection()
    cursor = connection.cursor()

    set_search_path(connection, cursor)

    transaction_data = load_csv(file_path)[1:]  # Skip header
    upload_transaction_data(connection, cursor, transaction_data)

    connection.close()


if __name__ == "__main__":
    TEST_PATH = "data/trucks/2024-11/4/12/combined_data.csv"
    main(TEST_PATH)
