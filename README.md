# Air Quality Stability — Projet Scientifique Reproductible

Projet TP12 : pipeline de qualité de l'air avec tests automatisés et exercices de stabilité numérique.

## Prérequis

- Python 3.10+ (ou Conda/Mamba)
- Git

## Installation de l'environnement

```bash
# Création de l'environnement (mamba ou conda)
mamba env create -f environment.yml

# Activation
conda activate air_quality_stability
```

## Exécution en une commande

```bash
# Pipeline complet + tests unitaires
python -m pytest tests/ -v && python src/main.py
```

## Exercices de stabilité numérique

```bash
python exercises/exercise_6_1_sommation.py
python exercises/exercise_6_2_conditionnement.py
python exercises/exercise_6_3_inversion_vs_solve.py
```

## Structure du projet

```
tp/
├── configs/config.yaml      # Configuration externalisée
├── data/raw/                # Données brutes (exclues de Git)
├── data/processed/            # Données traitées
├── exercises/               # Exercices Partie 6
├── src/                     # Code source modulaire
├── tests/                   # Tests pytest
├── environment.yml          # Dépendances Conda
└── DOCUMENTATION.md         # Guide détaillé étape par étape
```

## Données

Placez vos fichiers CSV bruts dans `data/raw/`. Le fichier `air_quality.csv` d'exemple est ignoré par Git (voir `.gitignore`).
