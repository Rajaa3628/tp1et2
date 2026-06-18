# Air Quality Stability

Projet TP12 avec architecture simplifiée.

## Structure

```
tp/
├── app/              # Code métier
├── settings/         # Configuration YAML
├── dataset/          # Données CSV
├── numerics/         # Exercices stabilité numérique
├── spec/             # Tests pytest
├── run.py            # Point d'entrée unique
└── environment.yml
```

## Installation

```bash
mamba env create -f environment.yml
conda activate air_quality_stability
```

## Exécution

```bash
python -m pytest -v && python run.py
```

## Exercices numériques

```bash
python numerics/sommation.py
python numerics/conditionnement.py
python numerics/inversion.py
```

Voir `DOCUMENTATION.md` pour le détail de chaque étape.
