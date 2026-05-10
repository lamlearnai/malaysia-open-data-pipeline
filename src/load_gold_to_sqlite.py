from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "fuel_prices.db"

GOLD_FILES = {
    "gold_fuel_monthly_average": "gold_fuel_monthly_average_*.csv",
    "gold_fuel_latest_price": "gold_fuel_latest_price_*.csv",
    "gold_fuel_weekly_change": "gold_fuel_weekly_change_*.csv",
    "gold_fuel_data_quality_report": "gold_fuel_data_quality_report_*.csv",
}

def get_latest_file(pattern: str) -> Path:
    files = list(GOLD_DIR.glob(pattern))

    if not files:
        raise FileNotFoundError(f"No file found for pattern: {pattern}")

    latest_file = max(files, key=lambda file: file.stat().st_mtime)
    return latest_file

def load_csv_to_sqlite(csv_path: Path, table_name: str, connection) -> None:
    df = pd.read_csv(csv_path)

    df.to_sql(
        name=table_name,
        con=connection,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into table: {table_name}")

def main():
    print("Loading gold CSV files into SQLite database...")
    print(f"Database path: {DATABASE_PATH}")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        for table_name, file_pattern in GOLD_FILES.items():
            latest_file = get_latest_file(file_pattern)

            print(f"\nReading: {latest_file}")
            load_csv_to_sqlite(latest_file, table_name, connection)

        print("\nAll gold tables loaded successfully.")

    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()