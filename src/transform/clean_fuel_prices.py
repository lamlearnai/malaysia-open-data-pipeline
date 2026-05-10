from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"
SILVER_DIR = PROJECT_ROOT / "data" / "silver"
SILVER_DIR.mkdir(parents=True, exist_ok=True)


def get_latest_bronze_file() -> Path:
    files = list(BRONZE_DIR.glob("fuel_prices_raw_*.csv"))

    if not files:
        raise FileNotFoundError("No bronze fuel price CSV file found.")

    latest_file = max(files, key=lambda file: file.stat().st_mtime)
    return latest_file


def clean_fuel_prices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Convert date column from text into proper date format
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert fuel price columns into numeric format
    fuel_columns = [
        "ron95",
        "ron97",
        "diesel",
        "ron95_skps",
        "ron95_budi95",
        "diesel_eastmsia"
    ]

    for column in fuel_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Keep only actual fuel price rows.
    # Why? Because "change" rows can be negative.
    # Actual fuel prices should never be negative.
    df = df[df["series_type"].astype(str).str.lower().str.strip() == "level"].copy()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Sort from oldest date to newest date
    df = df.sort_values("date")

    return df


def validate_fuel_prices(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Silver data is empty after cleaning.")

    if df["date"].isnull().sum() > 0:
        raise ValueError("Date column contains invalid or missing dates.")

    core_columns = ["ron95", "ron97", "diesel", "diesel_eastmsia"]

    for column in core_columns:
        if df[column].isnull().sum() > 0:
            raise ValueError(f"{column} contains missing values.")

        if (df[column] < 0).sum() > 0:
            raise ValueError(f"{column} contains negative fuel prices.")


def save_silver_data(df: pd.DataFrame) -> Path:
    today = datetime.today().strftime("%Y-%m-%d")
    output_path = SILVER_DIR / f"fuel_prices_clean_{today}.csv"

    df.to_csv(output_path, index=False)

    return output_path


def main():
    print("Cleaning fuel price bronze data...")

    bronze_file = get_latest_bronze_file()
    print(f"Reading bronze file: {bronze_file}")

    raw_df = pd.read_csv(bronze_file)

    print("\nSeries types before cleaning:")
    print(raw_df["series_type"].value_counts())

    clean_df = clean_fuel_prices(raw_df)

    print("\nSeries types after cleaning:")
    print(clean_df["series_type"].value_counts())

    print("\nRows with negative ron95 after cleaning:")
    print(clean_df[clean_df["ron95"] < 0].head())

    validate_fuel_prices(clean_df)

    output_path = save_silver_data(clean_df)

    print(f"\nRaw rows: {len(raw_df)}")
    print(f"Clean rows: {len(clean_df)}")
    print(f"Silver file saved to: {output_path}")
    print(f"File exists: {output_path.exists()}")


if __name__ == "__main__":
    main()