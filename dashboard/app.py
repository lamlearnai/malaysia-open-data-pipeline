from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "database" / "fuel_prices.db"

def run_query(query: str) -> pd.DataFrame:
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        df = pd.read_sql_query(query, connection)
        return df

    finally:
        connection.close()

def load_monthly_average() -> pd.DataFrame:
    query = """
    SELECT month, ron95, ron97, diesel, diesel_eastmsia
    FROM gold_fuel_monthly_average
    ORDER BY month;
    """
    return run_query(query)

def load_latest_price() -> pd.DataFrame:
    query = """
    SELECT date, ron95, ron97, diesel, diesel_eastmsia
    FROM gold_fuel_latest_price;
    """

    return run_query(query)

def load_quality_report() -> pd.DataFrame:
    query = """
    SELECT check_name, status, value, expected, checked_at
    FROM gold_fuel_data_quality_report;
    """

    return run_query(query)

def main():
    st.set_page_config(
        page_title="Malaysia Fuel Price Dashboard",
        layout="wide"
    )

    st.title("Malaysia Fuel Price Dashboard")
    st.write("This dashboard reads analytics-ready fuel price data from a SQLite database.")

    monthly_df = load_monthly_average()
    latest_df = load_latest_price()
    quality_df = load_quality_report()

    if monthly_df.empty:
        st.error("No monthly fuel price data found.")
        return

    st.subheader("Latest Fuel Price")

    latest_record = latest_df.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("RON95", f"RM {latest_record['ron95']:.2f}")
    col2.metric("RON97", f"RM {latest_record['ron97']:.2f}")
    col3.metric("Diesel", f"RM {latest_record['diesel']:.2f}")
    col4.metric("Diesel East Malaysia", f"RM {latest_record['diesel_eastmsia']:.2f}")

    st.caption(f"Latest record date: {latest_record['date']}")

    st.subheader("Data Quality Status")

    total_checks = len(quality_df)
    passed_checks = len(quality_df[quality_df["status"] == "PASS"])
    failed_checks = len(quality_df[quality_df["status"] == "FAIL"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Checks", total_checks)
    col2.metric("Passed Checks", passed_checks)
    col3.metric("Failed Checks", failed_checks)

    if failed_checks == 0:
        st.success("All data quality checks passed.")
    else:
        st.error("Some data quality checks failed.")

    st.dataframe(quality_df, use_container_width=True)

    st.subheader("Monthly Average Fuel Price Trend")

    chart_df = monthly_df.set_index("month")

    selected_columns = st.multiselect(
        "Choose fuel types to display",
        options=["ron95", "ron97", "diesel", "diesel_eastmsia"],
        default=["ron95", "ron97", "diesel"]
    )

    st.line_chart(chart_df[selected_columns])

    st.subheader("Monthly Average Data")

    st.dataframe(monthly_df, use_container_width=True)


if __name__ == "__main__":
    main()