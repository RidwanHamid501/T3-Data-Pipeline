'''Script that queries the database for a summary of the previous day's data'''
from os import environ
from datetime import datetime, timedelta
import redshift_connector as rc
from dotenv import load_dotenv
import altair as alt
import pandas as pd


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


def get_total_transactions(cursor: rc.Cursor, query_date: str) -> float:
    """Get total transaction count across all trucks"""
    cursor.execute("""
        SELECT COUNT(transaction_id) AS total_transaction_count
        FROM FACT_Transaction
        WHERE DATE(at) = %s
    """, (query_date,))
    result = cursor.fetchone()
    return round(result[0], 2) if result[0] else 0


def get_total_transaction_value(cursor: rc.Cursor, query_date: str) -> float:
    """Get total transaction value across all trucks"""
    cursor.execute("""
        SELECT SUM(total) AS total_transaction_revenue
        FROM FACT_Transaction
        WHERE DATE(at) = %s
    """, (query_date,))
    result = cursor.fetchone()
    return round(result[0], 2) if result[0] else 0


def get_payment_method_breakdown(cursor: rc.Cursor, query_date: str) -> list[dict[str, float]]:
    """Get total transaction value by payment method"""
    cursor.execute("""
        SELECT p.payment_method, SUM(f.total) AS total_revenue
        FROM FACT_Transaction f
        JOIN DIM_Payment_Method p ON f.payment_method_id = p.payment_method_id
        WHERE DATE(f.at) = %s
        GROUP BY p.payment_method
    """, (query_date,))
    return [
        {"payment_method": row[0], "total_revenue": round(row[1], 2)}
        for row in cursor.fetchall()
    ]


def get_truck_performance(cursor: rc.Cursor, query_date: str) -> list[dict[str, float]]:
    """Get total transaction value and count per truck"""
    cursor.execute("""
        SELECT t.truck_name, COUNT(f.transaction_id) AS transaction_count, SUM(f.total) AS total_revenue
        FROM FACT_Transaction f
        JOIN DIM_Truck t ON f.truck_id = t.truck_id
        WHERE DATE(f.at) = %s
        GROUP BY t.truck_name
    """, (query_date,))
    return [
        {
            "truck_name": row[0],
            "transaction_count": row[1],
            "total_revenue": round(row[2], 2)
        }
        for row in cursor.fetchall()
    ]


def get_daily_report(cursor: rc.Cursor, query_date: str) -> dict:
    """Generate daily report data by calling query functions."""
    report = {
        "total_transaction_count": get_total_transactions(cursor, query_date),
        "total_transaction_revenue": get_total_transaction_value(cursor, query_date),
        "payment_method_breakdown": get_payment_method_breakdown(cursor, query_date),
        "truck_performance": get_truck_performance(cursor, query_date)
    }
    return report


def create_pie_chart(data, labels, title):
    """Generate a pie chart using Altair"""
    df = pd.DataFrame({
        'Payment Method': labels,
        'Revenue': data
    })

    chart = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta('Revenue', stack=True),
        color=alt.Color('Payment Method', legend=None),
        tooltip=['Payment Method', 'Revenue']
    ).properties(
        title=title,
        width=300,
        height=300
    )

    return chart.to_html()


def generate_html(report_data: dict, date: str) -> str:
    payment_labels = [item['payment_method']
                      for item in report_data['payment_method_breakdown']]
    payment_data = [item['total_revenue']
                    for item in report_data['payment_method_breakdown']]
    payment_pie_chart_html = create_pie_chart(
        payment_data, payment_labels, "Revenue by Payment Method")

    return f"""
    <head>
        <title>Daily Report for {date}</title>
        <style>
            table {{ width: 50%;}}
            th, td {{ border: 1px solid #000; padding: 4px; }}
            th {{ background-color: lightgrey; }}
            tr {{ text-align: center; }}
        </style>
    </head>
    <body>
        <h1>Daily Report for {date}</h1>

        <h2>Total Transactions</h2>
        <p>{report_data['total_transaction_count']}</p>

        <h2>Total Revenue</h2>
        <p>£{report_data['total_transaction_revenue']}</p>

        <h2>Payment Method Breakdown</h2>
        <table>
            <tr><th>Payment Method</th><th>Total Revenue</th></tr>
            {''.join(f"<tr><td>{item['payment_method']}</td><td>£{item['total_revenue']}</td></tr>" for item in report_data['payment_method_breakdown'])}
        </table>

        <h2>Truck Performance</h2>
        <table>
            <tr><th>Truck Name</th><th>Transaction Count</th><th>Total Revenue</th></tr>
            {''.join(f"""<tr><td>{item['truck_name']}</td><td>{item['transaction_count']}</td><td>£{
                     item['total_revenue']}</td></tr>""" for item in report_data['truck_performance'])}
        </table>
        {payment_pie_chart_html}
    </body>

    """


def save_to_html(html_content, date) -> None:
    """Save report data to an HTML file"""
    filename = f"report_data_{date}.html"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Report saved to {filename}")


def lambda_handler(event, context) -> None:
    load_dotenv()
    connection = get_connection()
    cursor = connection.cursor()

    set_search_path(connection, cursor)

    previous_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    report_data = get_daily_report(cursor, previous_date)
    html_content = generate_html(report_data, previous_date)

    save_to_html(html_content, previous_date)

    connection.close()

    return {
        "statusCode": 200,
        "date": previous_date,
        "html_report": html_content
    }


if __name__ == "__main__":
    lambda_handler(1, 1)  # Test input
