# Airbnb Price Prediction — Paris

Projet de Data Science consacré à l'étude des prix affichés des logements Airbnb à Paris.
L'objectif est de construire progressivement un pipeline reproductible : acquisition des données, préparation, exploration, création de variables explicatives et prédiction du prix.

## Problématique

Dans quelle mesure les caractéristiques d'un logement et son environnement géographique peuvent-ils expliquer le prix d'une nuitée à Paris ?

Les données géographiques et événementielles pourront notamment servir à étudier l'influence de la proximité des monuments, des attractions, des transports et des événements sur les prix. Ces relations devront être mesurées à partir des données et ne sont pas considérées comme établies à ce stade.

## Données

### Inside Airbnb

Source principale du projet :
[Inside Airbnb](https://insideairbnb.com/get-the-data/)

Les fichiers Airbnb téléchargés depuis les URLs officielles sont convertis en Parquet et stockés localement dans `data/raw/airbnb/` :

- listings ;
- calendar ;
- reviews ;
- neighbourhoods.

### OpenStreetMap

Les points d'intérêt de Paris sont récupérés via l'API Overpass à partir d'une requête ciblant notamment les monuments, musées et attractions. Le résultat est enregistré dans :

```text
data/raw/poi/paris_poi.parquet
```

Une collecte vérifiée a permis de récupérer 499 éléments. Le nettoyage et le calcul des distances restent à réaliser.

### Transports

Un fichier de stations est présent dans `data/raw/poi/`. Il pourra être utilisé pour construire des variables d'accessibilité géographique.

### Ticketmaster

Une acquisition via la Discovery API Ticketmaster a été développée pour rechercher des événements musicaux à Paris sur la période étudiée. La requête testée n'a retourné aucun événement pour cette période ; cette source n'est donc pas encore exploitable pour l'analyse et pourra être remplacée ou complétée par une autre source.

## Pipeline prévu

```text
Sources externes
    ├── Inside Airbnb
    ├── OpenStreetMap / Overpass
    ├── Données de transport
    └── Événements
            ↓
      data/raw/
            ↓
   Nettoyage et préparation
            ↓
   Jointures et variables géographiques
            ↓
    Analyse exploratoire
            ↓
       Modèles de régression
```

Les acquisitions sont déjà amorcées. Le nettoyage, l'intégration complète des sources, le feature engineering et l'évaluation des modèles sont encore en cours de développement.

## Structure du dépôt

```text
.
├── .gitignore
├── configs/
│   └── project.yaml
├── data/
│   └── raw/
│       ├── airbnb/
│       │   ├── calendar.parquet
│       │   ├── listings.parquet
│       │   ├── listings_detailled.parquet
│       │   ├── neighbourhoods.parquet
│       │   └── reviews.parquet
│       ├── events/
│       │   └── paris_events.parquet
│       └── poi/
│           ├── paris_poi.parquet
│           └── train_station_scnf.parquet
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_features_engineering
│   ├── 03_EDA.ipynb
│   └── 04_ML.ipynb
├── src/
│   ├── __init__.py
│   ├── pipeline.py
│   └── data_acquisition/
│       ├── acquire_concerts_data.py
│       ├── acquire_osm_data_poi.py
│       └── data_acquisition_parquet.py
├── requirements.txt
└── README.md
```

Les fichiers `__pycache__`, `.DS_Store` et l'environnement `.venv` sont des fichiers locaux générés automatiquement et ne font pas partie de l'architecture du projet.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Pour utiliser l'API Ticketmaster, définir la clé dans l'environnement sans l'écrire dans le code :

```bash
export TICKETMASTER_API_KEY="votre_consumer_key"
```

## Exécution des acquisitions

Depuis la racine du projet :

```bash
python src/data_acquisition/data_acquisition_parquet.py
python src/data_acquisition/acquire_osm_data_poi.py
python src/data_acquisition/acquire_concerts_data.py
```

L'acquisition Ticketmaster peut ne produire aucun événement selon la période et la couverture historique de l'API.

## État du projet

- **Acquisition Airbnb :** implémentée avec conversion CSV vers Parquet.
- **Acquisition OpenStreetMap :** implémentée et testée pour les points d'intérêt de Paris.
- **Acquisition des stations :** implémentée
- **Acquisition Ticketmaster :** implémentée, mais aucun événement retourné sur la période testée.
- **Nettoyage et intégration :** en cours.
- **EDA et Machine Learning :** notebooks présents, résultats à compléter et documenter.

## Sources et licences

- [Inside Airbnb](https://insideairbnb.com/get-the-data/)
- [OpenStreetMap](https://www.openstreetmap.org/) et [Overpass API](https://overpass-api.de/)
- [Ticketmaster Discovery API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)

