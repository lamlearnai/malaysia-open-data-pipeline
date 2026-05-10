from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/malaysia_open_data"


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


def load_csv_to_postgres(csv_path: Path, table_name: str, engine) -> None:
    df = pd.read_csv(csv_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into PostgreSQL table: {table_name}")


def main():
    print("Loading gold CSV files into PostgreSQL database...")

    engine = create_engine(DATABASE_URL)

    for table_name, file_pattern in GOLD_FILES.items():
        latest_file = get_latest_file(file_pattern)

        print(f"\nReading: {latest_file}")
        load_csv_to_postgres(latest_file, table_name, engine)

    print("\nAll gold tables loaded into PostgreSQL successfully.")


if __name__ == "__main__":
    main()