from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from src.transformeurs import NettoyeurMaximumNights,ExtracteurAmenities,ImputerAvisAirbnb, ImputerCapacite


def preprocesseur(colonnes_numeriques, colonnes_categorielles):
    custom_transformer = Pipeline(steps=[
        ('nettoyage_nuits', NettoyeurMaximumNights()),
        ('amenities', ExtracteurAmenities(top_n=20)),
        ('reviews', ImputerAvisAirbnb()),
        ('capacite', ImputerCapacite())
    ])

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first'))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('numeric', numerical_transformer, colonnes_numeriques),
        ('cat', categorical_transformer, colonnes_categorielles)
    ], remainder=RobustScaler())

    return Pipeline(steps=[
        ('custom', custom_transformer),
        ('preprocessor', preprocessor)
    ])

def modeles():
    regressors = [
        ('Ridge', Ridge()),
        ('Random Forest', RandomForestRegressor(random_state=42, n_jobs=-1)),
        ('HistGradientBoosting', HistGradientBoostingRegressor(random_state=42))
    ]

    params_grid = {
        'Ridge': {
            'regressor__alpha': [0.1, 1.0, 10.0]
        },
        'Random Forest': {
            'regressor__max_depth': [15, 25],
            'regressor__n_estimators': [100]
        },
        'HistGradientBoosting': {
            'regressor__learning_rate': [0.05, 0.1],
            'regressor__max_iter': [100, 200]
        }
    }
    return regressors, params_grid