import pandas as pd
import numpy as np
from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin

class NettoyeurMaximumNights(BaseEstimator, TransformerMixin):
    """ 
    Plafonnement des valeurs aberrantes avec maximum de nuits à 365 jours
    """

    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df_temp = pd.DataFrame(X).copy()
        if 'maximum_nights' in df_temp.columns:
            df_temp.loc[df_temp['maximum_nights'] > 365, 'maximum_nights'] = 365
        return df_temp

class ExtracteurAmenities(BaseEstimator, TransformerMixin):
    """ 
    Nettoyage et extraction des n / équipements les plus communs sous forme de variable binaire.
    """

    
    def __init__(self, top_n=20):
        self.top_n = top_n

    def _convertir_en_liste(self, x):
        if pd.isna(x):
            return []
        texte_nettoye = str(x).replace('[', '').replace(']', '').replace('"', '').replace("'", "")
        return [equipement.strip() for equipement in texte_nettoye.split(',') if equipement.strip() != ""]

    def fit(self, X, y=None):
        df_temp = pd.DataFrame(X)
        if 'amenities' in df_temp.columns:
            listes = df_temp['amenities'].apply(self._convertir_en_liste)
            tous_les_items = [item for sous_liste in listes for item in sous_liste]
            self.top_amenities_ = [item for item, count in Counter(tous_les_items).most_common(self.top_n)]
        return self

    def transform(self, X):
        df_temp = pd.DataFrame(X).copy()
        if 'amenities' in df_temp.columns:
            listes = df_temp['amenities'].apply(self._convertir_en_liste)
            for am in getattr(self, 'top_amenities_', []):
                nom_colonne = f"amenity_{am.lower().replace(' ', '_').replace('/', '_')}"
                df_temp[nom_colonne] = listes.apply(lambda liste_eq: 1 if am in liste_eq else 0)
            df_temp = df_temp.drop(columns=['amenities'])
        return df_temp

class ImputerAvisAirbnb(BaseEstimator, TransformerMixin):
    """
    Imputations des scores d'évaluation par la médiane et création d'un indicateur binaire a_des_avis ou non
    """

    
    def fit(self, X, y=None):
        df_temp = pd.DataFrame(X)
        self.medianes_ = {} 
        colonnes_scores = [c for c in df_temp.columns if 'review_scores_' in str(c)]
        for col in colonnes_scores:
            self.medianes_[col] = df_temp[col].median()
        return self

    def transform(self, X):
        df_temp = pd.DataFrame(X).copy()
        
        if 'number_of_reviews' in df_temp.columns:
            df_temp['a_des_avis'] = (df_temp['number_of_reviews'] > 0).astype(int)
            
        if 'reviews_per_month' in df_temp.columns:
            df_temp['reviews_per_month'] = df_temp['reviews_per_month'].fillna(0)
            
        for col, med in getattr(self, 'medianes_', {}).items():
            if col in df_temp.columns:
                df_temp[col] = df_temp[col].fillna(med)
                
        return df_temp

class ImputerCapacite(BaseEstimator, TransformerMixin):
    """
    Remplace les Nan du nombre de lits par la médiane calculée sur le jeu d'entraînement en fonction de la capacité d'accueil de la variable accommodate
    """
    
    def fit(self, X, y=None):
        df_temp = pd.DataFrame(X)
        if 'beds' in df_temp.columns and 'accommodates' in df_temp.columns:
            self.lits_par_capacite_ = df_temp.groupby('accommodates')['beds'].median().to_dict()
        return self

    def transform(self, X):
        df_temp = pd.DataFrame(X).copy()
        
        if 'bedrooms' in df_temp.columns:
            df_temp['bedrooms'] = df_temp['bedrooms'].fillna(1)
            
        if 'beds' in df_temp.columns and 'accommodates' in df_temp.columns:
            # Mapping pur Pandas, avec fallback à 1
            dictionnaire_lits = getattr(self, 'lits_par_capacite_', {})
            lits_imputes = df_temp['accommodates'].map(dictionnaire_lits)
            df_temp['beds'] = df_temp['beds'].fillna(lits_imputes).fillna(1)
            
        return df_temp
