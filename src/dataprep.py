import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

def preparer_listings(chemin_fichier):

    """
    Sélection des variables pertinentes et traitement sur la target prix et binarisation de superhost
    """ 
    
    df = pd.read_parquet(chemin_fichier)
    colonnes_a_garder = [
        'id', 'property_type', 'room_type', 'accommodates', 'bedrooms', 'beds', 'amenities',
        'latitude', 'longitude', 'neighbourhood_cleansed', 'price', 'minimum_nights', 'maximum_nights',
        'host_is_superhost', 'host_identity_verified', 'host_listings_count', 'hosts_time_as_host_years',
        'number_of_reviews', 'number_of_reviews_ltm', 'reviews_per_month', 'review_scores_rating',
        'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
        'review_scores_communication', 'review_scores_location', 'review_scores_value',
        'availability_30', 'availability_60', 'availability_90', 'availability_365'
    ]
    colonnes_presentes = [c for c in colonnes_a_garder if c in df.columns]
    df = df[colonnes_presentes].copy()

    for col in ['host_is_superhost', 'host_identity_verified']:
        if col in df.columns:
            df[col] = df[col].map({'t': 1, 'f': 0, True: 1, False: 0})

    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).str.replace('$', '', regex=False)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna(subset=['price'])
        df = df[df['price'] > 0]
        
    return df

def feature_engineering_calendrier(chemin_fichier):

    """
    Calcul du taux d'occupation
    """ 

    
    df_cal = pd.read_parquet(chemin_fichier)
    df_cal['est_dispo'] = (df_cal['available'] == 't').astype(int)
    
    stats = df_cal.groupby('listing_id').agg(
        jours_totaux=('date', 'count'),
        jours_dispos=('est_dispo', 'sum')
    ).reset_index()
    
    stats['taux_occupation'] = 1 - (stats['jours_dispos'] / stats['jours_totaux'])
    return stats[['listing_id', 'taux_occupation']]

def calcul_distance_metro(df_logements, chemin_stations):
    """
    Calcul de la distance du logement à la station de métro la plus proche
    """ 
    df_stations = pd.read_parquet(chemin_stations)
    df_geo = df_logements.dropna(subset=['latitude', 'longitude']).copy()
    
    coords_stations = df_stations['Geo Point'].str.split(',', expand=True).astype(float)
    
    rad_logements = np.radians(df_geo[['latitude', 'longitude']].values)
    rad_stations = np.radians(coords_stations.values)
    
    arbre = cKDTree(rad_stations)
    distances, _ = arbre.query(rad_logements, k=1)
    
    df_geo['distance_metro_m'] = np.round(distances * 6371000, 1)
    return df_logements.merge(df_geo[['id', 'distance_metro_m']], on='id', how='left')

def charger_et_preparer_donnees(chemin_airbnb, chemin_poi):

    """
    Préparation du dataframe final à partir des traitements précédents
    """ 
    
    df_listings = preparer_listings(chemin_airbnb / "listings_detailled.parquet")
    df_calendrier = feature_engineering_calendrier(chemin_airbnb / "calendar.parquet")

    df_final = df_listings.merge(df_calendrier, left_on='id', right_on='listing_id', how='left')
    df_final = df_final.drop(columns=['listing_id'], errors='ignore')
    df_final = calcul_distance_metro(df_final, chemin_poi / "train_station_scnf.parquet")
    
    return df_final
