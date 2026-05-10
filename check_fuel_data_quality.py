from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
GOLD_DIR.mkdir(parents=True, exist_ok=True)


CORE_COLUMNS = ["date", "ron95", "ron97", "diesel", "diesel_eastmsia"]


def get_latest_silver_file() -> Path:
    files = list(SILVER_DIR.glob("fuel_prices_clean_*.csv"))

    if not files:
        raise FileNotFoundError("No silver fuel price CSV file found.")

    latest_file = max(files, key=lambda file: file.stat().st_mtime)
    return latest_file


def create_quality_check(check_name: str, passed: bool, value, expected: str) -> dict:
    return {
        "check_name": check_name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "expected": expected,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def run_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    checks = []

    checks.append(
        create_quality_check(
            check_name="row_count_greater_than_zero",
            passed=len(df) > 0,
            value=len(df),
            expected="More than 0 rows"
        )
    )

    checks.append(
        create_quality_check(
            check_name="no_duplicate_rows",
            passed=df.duplicated().sum() == 0,
            value=int(df.duplicated().sum()),
            expected="0 duplicate rows"
        )
    )

    for column in CORE_COLUMNS:
        missing_count = int(df[column].isnull().sum())

        checks.append(
            create_quality_check(
                check_name=f"no_missing_{column}",
                passed=missing_count == 0,
                value=missing_count,
                expected="0 missing values"
            )
        )

    price_columns = ["ron95", "ron97", "diesel", "diesel_eastmsia"]

    for column in price_columns:
        negative_count = int((df[column] < 0).sum())

        checks.append(
            create_quality_check(
                check_name=f"no_negative_{column}",
                passed=negative_count == 0,
                value=negative_count,
                expected="0 negative values"
            )
        )

    return pd.DataFrame(checks)


def save_quality_report(df: pd.DataFrame) -> Path:
    today = datetime.today().strftime("%Y-%m-%d")
    output_path = GOLD_DIR / f"gold_fuel_data_quality_report_{today}.csv"

    df.to_csv(output_path, index=False)

    return output_path


def main():
    print("Running fuel price data quality checks...")

    silver_file = get_latest_silver_file()
    print(f"Reading silver file: {silver_file}")

    silver_df = pd.read_csv(silver_file)

    quality_df = run_quality_checks(silver_df)
    output_path = save_quality_report(quality_df)

    print("\nData Quality Result:")
    print(quality_df)

    failed_checks = quality_df[quality_df["status"] == "FAIL"]

    if not failed_checks.empty:
        raise ValueError("Some data quality checks failed.")

    print(f"\nQuality report saved to: {output_path}")
    print(f"File exists: {output_path.exists()}")


if __name__ == "__main__":
    main()