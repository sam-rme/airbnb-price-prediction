# Prédiction de Prix Airbnb 

Ce projet vise à prédire le prix par nuit de logements Airbnb à Paris

Arborescence :

- dossier data : Avec les données brutes dans raw et les donnés du dataprep.py et le meilleure modèle dans processed.
- dataprep.py : Script de feature engineering et fusion des données.
- transformeurs.py : Classes personnalisées pour le nettoyage des variables.
- pipeline.py : Preprocesseur et GridSearch.
- modele.py : Execute le tout. (python modele.py sur le bash)

## EDA

1. Le prix des logements étant très asymétrique on a fait une transformation logarithmique avec np.log1p pour rapprocher la distribution d'une loi normale.
2. Création de la variable variable taux_occupation calculée à partir des données de calendrier.
3. Utilisation de cKDTree pour calculer la distance en m entre chaque logement et la station de métro la plus prochee.

## Transformateurs

- NettoyeurMaximumNights: On a remarqué pendant l'entraînement que le R2 atteignait des scores très négatifs et on a remarqué que maximum_nights atteignait des valeurs aberrantes au lieu de 365 jours, on l'a plafonné (voire Modeles)
- ExtracteurAmenities : Nettoyage et extraction des n / 20 équipements les plus communs sous forme de variable binaire.
- ImputerCapacite : Remplace les Nan du nombre de lits par la médiane calculée sur le jeu d'entraînement en fonction de la capacité d'accueil accommodate).
- ImputerAvisAirbnb : On a imputé les scores d'évaluation par la médiane et créer un indicateur binaire a_des_avis pour faire la différence entre les logements non notés de ceux mal notés.

## Modeles

- Ridge 
- Random Forest Regressor
- HistGradientBoosting Regressor

# Résultat final :
Le modèle HistGradientBoosting offre les meilleures performances (MAE le plus bas). Le meilleur modèle a été sauvegardé au format joblib.

## importances variables

On a calculé la le features importances avec permutation_importance (feature_importance indisponible pour HistGradientBoosting)

Les 5 variables qui ont le plus contribué sont :

1. minimum_nights : C'est la variable qui impacte le plus le prix. L'intuition c'est que les logements qui proposent un nombre de nuits élevés sont destinés à une clientèle moins premium, ça cible les touristes avec un prix par nuit certainement élevé.
   Quand le minimum est plus élevé on s'attends à ce que le client reste plus longtemps donc des locaux.
   
3. accommodates et bedrooms : La capacité d'accueil et le nombre de chambres pour des raisons logiques, c'est le m2 qui dicte le prix sur Paris et l'emplacement.
4. latitude et longitude : De manière logique l'emplacement comme on l'a constaté dans l'EDA (le centre de Paris) .
5. amenities : La présence d'équipements a bien un impact mesurable mais reste secondaire.
