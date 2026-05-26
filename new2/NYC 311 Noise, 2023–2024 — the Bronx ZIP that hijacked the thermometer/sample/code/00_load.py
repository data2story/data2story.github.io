"""00_load.py — read the 1 GB raw CSV once, write a slim parquet cache.

Subsequent scripts read `cache.parquet` (a tenth the size, already typed and
date-parsed) instead of re-reading the source CSV. The cache file lives in
this same `code/` directory so it travels with the project.

Produces no `ana_xx` finding — this is pure infrastructure.
"""
from pathlib import Path
import pandas as pd

DATA = Path(r"D:/AI/journalist agent review/phase2/datasets/nyc_311_noise")
CACHE = Path(__file__).parent / "cache.parquet"

USECOLS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "location_type",
    "incident_zip",
    "status",
    "resolution_description",
    "community_board",
    "borough",
    "open_data_channel_type",
    "latitude",
    "longitude",
]

DTYPES = {
    "unique_key": "string",
    "agency": "category",
    "agency_name": "category",
    "complaint_type": "category",
    "descriptor": "category",
    "location_type": "category",
    "incident_zip": "string",
    "status": "category",
    "resolution_description": "string",
    "community_board": "category",
    "borough": "category",
    "open_data_channel_type": "category",
}


def main() -> None:
    print("reading CSV (1 GB)...")
    df = pd.read_csv(
        DATA / "noise_complaints_2023_2024.csv",
        usecols=USECOLS,
        dtype=DTYPES,
        parse_dates=["created_date", "closed_date"],
        low_memory=False,
    )
    print(f"  rows: {len(df):>9,}    columns: {len(df.columns)}")
    print(f"  date range: {df['created_date'].min()}  →  {df['created_date'].max()}")
    print(f"writing parquet cache → {CACHE}")
    df.to_parquet(CACHE, index=False, compression="snappy")
    print(f"  cache size: {CACHE.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
