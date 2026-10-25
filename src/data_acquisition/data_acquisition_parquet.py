"""Generates the data in paruqet format using the doawnload links of the csv from Inside AirBnb and from other soruces for POI (Point of Interest)"""

#Imports
import pandas as pd
from pathlib import Path
import csv
import json
from datetime import datetime, timezone

import requests

# Project configuration

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
DATA_URLS = {
    "listings" :"https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/visualisations/listings.csv",
    "listings_detailled" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/listings.csv.gz",
    "calendar" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/calendar.csv.gz",
    "reviews" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/visualisations/reviews.csv",
    "neighbourhoods" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/visualisations/neighbourhoods.csv",

    # POI
    "train_station_scnf" :"https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/emplacement-des-gares-idf-data-generalisee/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%2C",

}


POI_file_names =["train_station_scnf",]

def convert_csv_to_parquet(urls:dict[str, str], output_dir : Path) -> None:
    """ Prends un lien de DL d'un fichier csv et l'enregistre au format parquet dans /data/raw pour gagner le place"""
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_names = urls.keys()
    for name,url in urls.items():
        df = pd.read_csv(url, engine='python')
        if name in POI_file_names : 
            output_file = output_dir / "poi" / f"{name}.parquet"
        else: 
            output_file = output_dir / "airbnb" / f"{name}.parquet"
        df.to_parquet(output_file, engine="pyarrow", index=False)
    print("Tous les fichiers ont été enregistrés sous le format parquet")



if __name__ == "__main__":
    convert_csv_to_parquet(DATA_URLS, OUTPUT_DIR)