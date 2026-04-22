# Détection de Fraude - BNP Paribas Personal Finance

Ce dépôt contient le code et l'analyse réalisés dans le cadre du [Challenge Data ENS](https://challengedata.ens.fr) proposé 
par BNP Paribas Personal Finance. 

Ce projet a été mené au cours de mon Master en Mathématiques et Applications (spécialité Ingénierie Statistique, Actuariat et 
Data Science) à l'Université Paris-Saclay. Il vise à mettre en pratique des méthodes avancées de machine learning sur des données 
transactionnelles réelles.

## Objectif du projet

Le but de ce challenge est de **démasquer les fraudeurs**. Il s'agit d'un problème d'apprentissage supervisé (classification 
binaire) où l'objectif est d'identifier si une opération est frauduleuse en se basant sur le contenu d'un panier d'achat. 

Les données fournies contiennent des informations détaillées sur les articles achetés (prix, marques, modèles, etc.) pouvant aller 
jusqu'à 24 articles par transaction.

## Structure du projet

* `notebooks/Projet - BNP Paribas PF.ipynb` : Le notebook principal contenant l'exploration des données (EDA),
le preprocessing (gestion des valeurs manquantes, encodage), et l'entraînement des modèles de classification.
* `data/` : Dossier prévu pour héberger les fichiers d'entraînement et de test (`X_test.csv`, `Y_train.csv`, etc.).  
*Note : Les données ne sont pas hébergées sur ce dépôt pour des raisons de taille.*

## Technologies et Modèles utilisés

L'analyse et la modélisation ont été réalisées en **Python**.
* **Manipulation de données :** `pandas`, `numpy`
* **Visualisation :** `matplotlib`, `seaborn`
* **Machine Learning :** `scikit-learn`, `xgboost`, `lazypredict`
* **Techniques clés :** * Restructuration de données complexes (transformation Wide to Long).
    * Imputation des données manquantes.
    * Réduction de dimension (PCA).
    * Évaluation des performances via la métrique **PR-AUC** (Area Under the Precision-Recall Curve), particulièrement adaptée
    * aux jeux de données très déséquilibrés comme la détection de fraude.

## Comment reproduire l'analyse

1. Clonez ce repository :
   ```bash
   git clone [https://github.com/jean-guillaum3/bnp-paribas-fraud-detection.git](https://github.com/jean-guillaum3/bnp-paribas-fraud-detection.git)
   cd bnp-paribas-fraud-detection
