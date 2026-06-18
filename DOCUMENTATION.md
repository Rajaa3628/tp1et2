# Documentation TP12

Guide étape par étape du projet scientifique reproductible.

## Architecture simplifiée

| Dossier | Rôle | Ancien nom |
|---------|------|------------|
| `app/` | Code Python (preprocessing, utils) | `src/` |
| `settings/` | Fichier de configuration YAML | `configs/` |
| `dataset/` | Données CSV | `data/raw/` + `data/processed/` |
| `numerics/` | Exercices stabilité numérique | `exercises/` |
| `spec/` | Tests pytest | `tests/` |
| `results/` | Sorties générées | `outputs/` |
| `run.py` | Point d'entrée unique | `src/main.py` |

## Partie 1 — Environnement

Fichier `environment.yml` : Python 3.10 + numpy, pandas, scikit-learn, matplotlib, pyyaml, pytest.

```bash
mamba env create -f environment.yml
conda activate air_quality_stability
```

## Partie 2 — Prétraitement

Fichier `app/preprocessing.py` :
- Imputation des valeurs manquantes par la **médiane**
- Clipping des outliers via **IQR** (bornes : Q1 − 1.5×IQR, Q3 + 1.5×IQR)

Configuration dans `settings/config.yaml`.

## Partie 3 — Tests

Fichier `spec/test_preprocessing.py` : vérifie que `split_and_scale` produit le même résultat avec la même graine.

```bash
python -m pytest -v
```

## Partie 4 — Gitignore

Exclut `dataset/*` (sauf `.gitkeep`), caches Python, `results/`, fichiers CSV.

## Partie 5 — Pipeline

Fichier `run.py` :
- Backend Matplotlib `Agg` (mode serveur)
- Charge `settings/config.yaml`
- Exécute nettoyage + partitionnement

```bash
python run.py
```

## Partie 6 — Stabilité numérique

| Script | Contenu |
|--------|---------|
| `numerics/sommation.py` | Sommation naïve vs Kahan |
| `numerics/conditionnement.py` | Matrice de Hilbert, κ(A), perturbation |
| `numerics/inversion.py` | `inv(A)@b` vs `solve(A,b)` sur n=4000 |

## Commande unique

```bash
python -m pytest -v && python run.py
```

## Questions de réflexion (réponses)

1. **Ratio de gain (6.3)** : le solveur direct est ~3× plus rapide car il évite le calcul complet de A⁻¹ (O(n³) inutile pour une seule solution).

2. **Chiffres significatifs** : avec κ=10¹³ et ε_mach≈10⁻¹⁶, environ **3 chiffres** sont fiables ; le reste est du bruit numérique.

3. **Éthique** : modifier des données brutes sans traçabilité viole la reproductibilité scientifique.
