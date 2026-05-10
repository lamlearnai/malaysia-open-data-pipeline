from pathlib import Path
from datetime import datetime
import logging
import subprocess
import sys
import time


PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_filename = datetime.now().strftime("pipeline_run_%Y-%m-%d_%H-%M-%S.log")
LOG_PATH = LOG_DIR / log_filename


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)


PIPELINE_STEPS = [
    "src/extract/extract_fuel_prices.py",
    "src/transform/clean_fuel_prices.py",
    "src/transform/build_gold_fuel_prices.py",
    "src/load_gold_to_sqlite.py",
]


def run_step(script_path: str) -> None:
    full_path = PROJECT_ROOT / script_path

    logging.info("=" * 80)
    logging.info(f"Starting step: {script_path}")

    start_time = time.time()

    subprocess.run(
        [sys.executable, str(full_path)],
        cwd=PROJECT_ROOT,
        check=True
    )

    duration = round(time.time() - start_time, 2)

    logging.info(f"Completed step: {script_path}")
    logging.info(f"Duration: {duration} seconds")


def main():
    logging.info("Starting Malaysia Open Data Pipeline")
    logging.info(f"Project root: {PROJECT_ROOT}")
    logging.info(f"Log file: {LOG_PATH}")

    pipeline_start = time.time()

    try:
        for step in PIPELINE_STEPS:
            run_step(step)

        total_duration = round(time.time() - pipeline_start, 2)

        logging.info("=" * 80)
        logging.info("Pipeline completed successfully")
        logging.info(f"Total duration: {total_duration} seconds")

    except subprocess.CalledProcessError as error:
        logging.error("=" * 80)
        logging.error("Pipeline failed")
        logging.error(f"Failed command: {error.cmd}")
        logging.error(f"Return code: {error.returncode}")
        raise


if __name__ == "__main__":
    main()