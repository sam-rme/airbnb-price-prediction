"""Collects events from ticketmaster API, however the API does not give any events at the perido selected i'll try to pick data from another source"""

import os
from pathlib import Path
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "events"
RAW_PARQUET_PATH = RAW_DIR / "paris_events.parquet"

# API configuration
API_KEY = os.environ.get("TICKETMASTER_API_KEY", "").strip()

if not API_KEY:
    raise RuntimeError(
        "TICKETMASTER_API_KEY est absente. "
        "Définis-la avant d'exécuter le script."
    )

params = {"apikey": API_KEY, 
          "city" : 
          "startDateTime": "2026-09-16T00:00:00Z", 
          "endDateTime": "2026-12-15T00:00:00Z"} # Dates correponding to the date of our listings checkin dates

API_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def acquire_events_data() -> None:
    response = requests.get(
        API_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    events = payload.get("_embedded", {}).get("events", [])
    print(events)

    RAW_DIR.mkdir(parents = True, exist_ok=True)
    pd.DataFrame(events).to_parquet(RAW_PARQUET_PATH, engine="pyarrow", index=False)
    print(f"{len(events)} events have been saved")



if __name__ == "__main__":
    acquire_events_data()

#0 events have been saved = Unfortunetely there is no corresponding events or concerts during the period of our data from the airbnb listings.