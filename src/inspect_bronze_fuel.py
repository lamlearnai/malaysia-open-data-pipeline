from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"


def get_latest_bronze_file() -> Path:
    files = list(BRONZE_DIR.glob("fuel_prices_raw_*.csv"))

    if not files:
        raise FileNotFoundError("No bronze fuel price CSV file found.")

    latest_file = max(files, key=lambda file: file.stat().st_mtime)
    return latest_file


def main():
    latest_file = get_latest_bronze_file()

    print(f"Reading file: {latest_file}")

    df = pd.read_csv(latest_file)

    print("\n--- Shape ---")
    print(df.shape)

    print("\n--- Columns ---")
    print(df.columns.tolist())

    print("\n--- First 5 rows ---")
    print(df.head())

    print("\n--- Data types ---")
    print(df.dtypes)

    print("\n--- Missing values ---")
    print(df.isnull().sum())

    print("\n--- Duplicate rows ---")
    print(df.duplicated().sum())


if __name__ == "__main__":
    main()