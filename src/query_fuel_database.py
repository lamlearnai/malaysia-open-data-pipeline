from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "database" / "fuel_prices.db"


def run_query(query: str) -> pd.DataFrame:
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        df = pd.read_sql_query(query, connection)
        return df

    finally:
        connection.close()


def main():
    print("Querying fuel price database...")
    print(f"Database path: {DATABASE_PATH}")

    latest_price_query = """
    SELECT *
    FROM gold_fuel_latest_price;
    """

    monthly_average_query = """
    SELECT month, ron95, ron97, diesel, diesel_eastmsia
    FROM gold_fuel_monthly_average
    ORDER BY month DESC
    LIMIT 10;
    """

    highest_ron97_query = """
    SELECT month, ron97
    FROM gold_fuel_monthly_average
    ORDER BY ron97 DESC
    LIMIT 5;
    """

    print("\n--- Latest Fuel Price ---")
    print(run_query(latest_price_query))

    print("\n--- Latest 10 Monthly Average Records ---")
    print(run_query(monthly_average_query))

    print("\n--- Top 5 Highest Monthly Average RON97 Prices ---")
    print(run_query(highest_ron97_query))


if __name__ == "__main__":
    main()