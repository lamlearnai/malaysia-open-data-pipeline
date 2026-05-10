from pathlib import Path
from datetime import datetime

import pandas as pd
import requests

API_URL = "https://api.data.gov.my/data-catalogue"
DATASET_ID = "fuelprice"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "bronze"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_fuel_prices(limit: int = 1000) -> pd.DataFrame:
    params = {
        "id": DATASET_ID,
        "limit": limit
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)

    return df

def save_bronze_data(df: pd.DataFrame) -> Path:
    today = datetime.today().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"fuel_prices_raw_{today}.csv"

    df.to_csv(output_path, index=False)

    return output_path

def main():
    print("Extracting fuel price data...")

    df = extract_fuel_prices()
    output_path = save_bronze_data(df)

    print(f"Rows extracted: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()