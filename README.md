## Project Structure

```text
malaysia-open-data-pipeline/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── bronze/
│   │   └── .gitkeep
│   ├── silver/
│   │   └── .gitkeep
│   └── gold/
│       └── .gitkeep
│
├── database/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── screenshots/
│   ├── dashboard.png
│   └── pipeline_success.png
│
├── src/
│   ├── extract/
│   │   └── extract_fuel_prices.py
│   │
│   ├── transform/
│   │   ├── clean_fuel_prices.py
│   │   └── build_gold_fuel_prices.py
│   │
│   ├── inspect_bronze_fuel.py
│   ├── load_gold_to_sqlite.py
│   ├── query_fuel_database.py
│   └── run_pipeline.py
│
├── .gitignore
├── requirements.txt
└── README.md