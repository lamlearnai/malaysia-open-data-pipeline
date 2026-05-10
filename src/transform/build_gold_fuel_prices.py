from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
GOLD_DIR.mkdir(parents=True, exist_ok=True)


PRICE_COLUMNS = [
    "ron95",
    "ron97",
    "diesel",
    "diesel_eastmsia"
]


def get_latest_silver_file() -> Path:
    files = list(SILVER_DIR.glob("fuel_prices_clean_*.csv"))

    if not files:
        raise FileNotFoundError("No silver fuel price CSV file found.")

    latest_file = max(files, key=lambda file: file.stat().st_mtime)
    return latest_file


def prepare_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if df["date"].isnull().sum() > 0:
        raise ValueError("Date column contains invalid dates.")

    return df


def build_monthly_average(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_df = (
        df.groupby("month", as_index=False)[PRICE_COLUMNS]
        .mean()
        .round(3)
    )

    return monthly_df


def build_latest_price(df: pd.DataFrame) -> pd.DataFrame:
    latest_df = (
        df.sort_values("date")
        .tail(1)[["date"] + PRICE_COLUMNS]
        .copy()
    )

    return latest_df


def build_weekly_price_change(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("date").copy()

    for column in PRICE_COLUMNS:
        df[f"{column}_change"] = df[column].diff().round(3)

    change_columns = [f"{column}_change" for column in PRICE_COLUMNS]

    weekly_change_df = df[["date"] + PRICE_COLUMNS + change_columns]

    return weekly_change_df


def save_gold_data(df: pd.DataFrame, name: str) -> Path:
    today = datetime.today().strftime("%Y-%m-%d")
    output_path = GOLD_DIR / f"{name}_{today}.csv"

    df.to_csv(output_path, index=False)

    return output_path


def main():
    print("Building fuel price gold layer...")

    silver_file = get_latest_silver_file()
    print(f"Reading silver file: {silver_file}")

    silver_df = pd.read_csv(silver_file)
    silver_df = prepare_dates(silver_df)

    monthly_average_df = build_monthly_average(silver_df)
    latest_price_df = build_latest_price(silver_df)
    weekly_change_df = build_weekly_price_change(silver_df)

    monthly_path = save_gold_data(monthly_average_df, "gold_fuel_monthly_average")
    latest_path = save_gold_data(latest_price_df, "gold_fuel_latest_price")
    weekly_change_path = save_gold_data(weekly_change_df, "gold_fuel_weekly_change")

    print(f"\nSilver rows read: {len(silver_df)}")

    print(f"\nMonthly average rows: {len(monthly_average_df)}")
    print(f"Saved to: {monthly_path}")

    print(f"\nLatest price rows: {len(latest_price_df)}")
    print(f"Saved to: {latest_path}")

    print(f"\nWeekly change rows: {len(weekly_change_df)}")
    print(f"Saved to: {weekly_change_path}")


if __name__ == "__main__":
    main()