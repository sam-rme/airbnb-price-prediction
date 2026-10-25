"""Generates the data in paruqet format using the doawnload links of the csv from Inside AirBnb"""

#Imports
import pandas as pd
from pathlib import Path

# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
DATA_URLS = {
    "listings" :"https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/visualisations/listings.csv",
    "listings_detailled" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/listings.csv.gz",
    "calendar" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/calendar.csv.gz",
    "reviews" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/visualisations/reviews.csv",
    "neighbourhoods" : "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/visualisations/neighbourhoods.csv",
}


def convert_csv_to_parquet(urls:dict[str, str], output_dir : Path) -> None:
    """ Prends un lien de DL d'un fichier csv et l'enregistre au format parquet dans /data/raw pour gagner le place"""
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_names = urls.keys()
    for name,url in urls.items():
        df = pd.read_csv(url)
        output_file = output_dir / f"{name}.parquet"
        df.to_parquet(output_file, engine="pyarrow", index=False)
    print("Tous les fichiers ont été enregistrés sous le format parquet")



#Execution
def main() -> None:
    """Run the data acquisition pipeline."""

    convert_csv_to_parquet(DATA_URLS, OUTPUT_DIR)


if __name__ == "__main__":
    main()