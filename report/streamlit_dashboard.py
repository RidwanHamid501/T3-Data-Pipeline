"""Streamlit Dashboard app"""
from os import environ
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import redshift_connector as rc


def set_search_path(conn: rc.Connection, cursor: rc.Cursor) -> None:
    """Set search path for the database schema"""
    cursor.execute(f"SET search_path TO {environ['SCHEMA']}")
    conn.commit()


def get_connection():
    '''Retrieve connection'''
    return rc.connect(
        host=environ["HOST"],
        port=environ["PORT"],
        database=environ["DATABASE_NAME"],
        user=environ["USERNAME"],
        password=environ["PASSWORD"]
    )


def load_data(cursor):
    """Load data from the database and join truck names and payment methods"""
    query = """
        SELECT 
            t.at, 
            pm.payment_method, 
            t.total, 
            t.truck_id, 
            d.truck_name 
        FROM 
            FACT_Transaction t
        JOIN 
            DIM_Truck d ON t.truck_id = d.truck_id
        JOIN 
            DIM_Payment_Method pm ON t.payment_method_id = pm.payment_method_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    columns = ['at', 'payment_method', 'total', 'truck_id', 'truck_name']
    data = pd.DataFrame(rows, columns=columns)

    return data


def plot_transaction_counts(data):
    """Plot the total number of transactions per truck as a pie chart"""
    transaction_counts = data['truck_name'].value_counts()

    fig, ax = plt.subplots()
    ax.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%')
    st.write("### Total Number of Transactions per Truck")

    st.pyplot(fig)


def plot_payment_type_counts(data):
    """Plot the number of card and cash transactions for each truck"""
    payment_counts = data.groupby(
        ['truck_name', 'payment_method']).size().unstack(fill_value=0)

    st.write("### Number of Card and Cash Transactions per Truck")
    st.bar_chart(payment_counts)


def plot_daily_revenue(data):
    """Plot daily revenue for each truck as a line chart."""
    data['date'] = data['at'].dt.date

    daily_revenue = data.groupby(['date', 'truck_name'])[
        'total'].sum().unstack()

    st.write("### Daily Revenue for Each Truck")
    st.line_chart(daily_revenue)


def filtered_data_by_date(data):
    """Filter data by chosen dates"""
    data['day'] = data['at'].dt.date
    data['hour'] = data['at'].dt.hour

    selected_date_range = st.date_input(
        "Select Date Range",
        value=(data['day'].min(), data['day'].max())
    )

    start_date, end_date = selected_date_range
    filtered_data = data[(data['day'] >= start_date)
                         & (data['day'] <= end_date)]

    return filtered_data


def main(cursor):
    """Run streamlit app."""
    data = filtered_data_by_date(load_data(cursor))

    column_left, column_right = st.columns(2)

    with column_left:
        plot_payment_type_counts(data)

    with column_right:
        plot_transaction_counts(data)

    plot_daily_revenue(data)


if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    cursor_conn = connection.cursor()
    set_search_path(connection, cursor_conn)
    connection.commit()
    st.set_page_config(page_title="Truck Analysis Dashboard", layout="wide")

    main(cursor_conn)
