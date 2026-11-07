from pathlib import Path
import numpy as np
import pandas as pd
from tqdm import tqdm
import joblib # 1. Ajout de l'import
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from src.dataprep import charger_et_preparer_donnees
from src.pipeline import preprocesseur, modeles

chemin_base = Path(__file__).parent
chemin_airbnb = chemin_base / "data" / "raw" / "airbnb"
chemin_poi = chemin_base / "data" / "raw" / "poi"
chemin_sauvegarde = chemin_base / "data" / "processed"
chemin_sauvegarde.mkdir(parents=True, exist_ok=True)

def main():
    df_final = charger_et_preparer_donnees(chemin_airbnb, chemin_poi)
    df_final.to_parquet(chemin_sauvegarde / "master_airbnb.parquet", index=False)

    X = df_final[[
        'accommodates', 'bedrooms', 'beds', 'minimum_nights', 'maximum_nights',
        'host_is_superhost', 'host_listings_count', 'hosts_time_as_host_years',
        'number_of_reviews', 'number_of_reviews_ltm', 'reviews_per_month',
        'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
        'review_scores_value', 'availability_30', 'availability_60', 'availability_90',
        'availability_365', 'taux_occupation', 'distance_metro_m', 'latitude', 'longitude',
        'room_type', 'property_type', 'neighbourhood_cleansed', 'amenities'
    ]]
    y = np.log1p(df_final['price'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    colonnes_numeriques = [
        'accommodates', 'bedrooms', 'beds', 'minimum_nights', 'maximum_nights',
        'host_is_superhost', 'host_listings_count', 'hosts_time_as_host_years',
        'number_of_reviews', 'number_of_reviews_ltm', 'reviews_per_month',
        'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
        'review_scores_value', 'availability_30', 'availability_60', 'availability_90',
        'availability_365', 'taux_occupation', 'distance_metro_m'
    ]

    colonnes_categorielles = [
        'room_type', 'property_type', 'neighbourhood_cleansed'
    ]

    pipeline_preprocessor = preprocesseur(colonnes_numeriques, colonnes_categorielles)
    regressors, params_grid = modeles()

    results = {}
    modeles_entraines = {}

    for regressor_name, regressor in tqdm(regressors, desc="Entrainement/GridSearch"):
        pipeline_complet = Pipeline(steps=[
            ('preprocessor_step', pipeline_preprocessor),
            ('regressor', regressor)
        ])

        model = GridSearchCV(
            pipeline_complet, 
            params_grid[regressor_name], 
            cv=3, 
            scoring='r2', 
            n_jobs=-1, 
            error_score='raise'
        )
        
        model.fit(X_train, y_train)

        y_pred_log = model.predict(X_test)
        y_test_euros = np.expm1(y_test)
        y_pred_euros = np.expm1(y_pred_log)

        modeles_entraines[regressor_name] = model.best_estimator_

        results[regressor_name] = {
            'Best params': model.best_params_, 
            'R2 on train': round(r2_score(y_train, model.best_estimator_.predict(X_train)), 3),
            'R2 CV': round(model.best_score_, 3),
            'R2 on test': round(r2_score(y_test, y_pred_log), 3),
            'MAE in Euros': round(mean_absolute_error(y_test_euros, y_pred_euros), 2)
        }

    df_results = pd.DataFrame(results)
    print(df_results)

    meilleur_modele = df_results.loc['MAE in Euros'].idxmin()
    meilleur_modele = modeles_entraines[meilleur_modele]

    chemin_modele = chemin_sauvegarde / "modele_airbnb_paris.joblib"
    joblib.dump(meilleur_modele, chemin_modele)
    print("Modèle sauvegardé dans :", chemin_modele")

if __name__ == "__main__":
    main()