"""Collect points of interest from OpenStreetMap through the Overpass API."""

from pathlib import Path

import pandas as pd
import requests


# API configuration
API_URL = "https://lz4.overpass-api.de/api/interpreter"
QUERY = r"""
[out:json][timeout:120];

area["ref:INSEE"="75056"]
   ["boundary"="administrative"]
   ["admin_level"="8"]->.paris;

(
 nwr["historic"~"^(monument)$"]["name"](area.paris);
 nwr["tourism"~"^(attraction|museum)$"]["name"](area.paris);
);

out center;
"""


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "poi"
RAW_PARQUET_PATH = RAW_DIR / "paris_poi.parquet"
USER_AGENT = "AirbnbDataScienceProject"


def acquire_osm_data() -> None:
    """Retrieve the OpenStreetMap response data for munuments and attraction in paris and save it in raw Parquet format."""
    response = requests.post(
        API_URL,
        data={"data": QUERY},
        headers={"User-Agent": USER_AGENT},
        timeout=150,
    )
    response.raise_for_status()

    payload = response.json()
    elements = payload.get("elements", [])

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(elements).to_parquet(RAW_PARQUET_PATH, engine="pyarrow", index=False)
    print(f"{len(elements)} éléments enregistrés dans {RAW_PARQUET_PATH}")


if __name__ == "__main__":
    acquire_osm_data()