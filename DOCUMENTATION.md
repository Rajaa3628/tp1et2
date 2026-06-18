# Documentation TP12 — Guide étape par étape

Ce document explique chaque partie du TP **Construction d'un Projet Scientifique Reproductible et Analyse de Stabilité Numérique**.

---

## Partie 1 : Isolation et Gestion de l'Environnement

### Objectif

Isoler les dépendances logicielles pour garantir que le projet s'exécute de la même manière sur toute machine.

### Fichier `environment.yml`

L'environnement Conda `air_quality_stability` est configuré avec :

| Paquet | Rôle |
|--------|------|
| `python=3.10` | Version Python fixée |
| `numpy` | Calcul numérique |
| `pandas` | Manipulation de données tabulaires |
| `scikit-learn` | Prétraitement et modèles ML |
| `matplotlib` | Visualisation |
| `pyyaml` | Lecture de fichiers de configuration |
| `pytest` | Tests unitaires |
| `logging-config` | Configuration des logs (pip) |

### Commandes d'installation

```bash
# 1. Création de l'environnement
mamba env create -f environment.yml
# Alternative : conda env create -f environment.yml

# 2. Activation
conda activate air_quality_stability
```

**Pourquoi ?** Sans fichier d'environnement, un collaborateur ne sait pas quelles versions installer. Le syndrome *« ça marche sur ma machine »* disparaît quand les dépendances sont déclarées explicitement.

---

## Partie 2 : Configuration et Modularité du Pipeline

### Objectif

Externaliser les hyperparamètres et implémenter le prétraitement des données de qualité de l'air.

### Fichier `configs/config.yaml`

Tous les paramètres (graine aléatoire, chemins, seuils) sont centralisés dans un fichier YAML, jamais codés en dur dans le Python.

### Fichier `src/preprocessing.py`

#### Imputation par la médiane

Pour chaque colonne contenant des valeurs manquantes (`NaN`), on calcule la médiane et on remplace les trous :

```python
median_value = df_clean[col].median()
df_clean[col] = df_clean[col].fillna(median_value)
```

La médiane est robuste aux valeurs extrêmes, contrairement à la moyenne.

#### Détection des outliers par IQR

Pour chaque colonne numérique (sauf la cible `pm25`) :

1. Calculer Q1 (25e percentile) et Q3 (75e percentile)
2. Calculer IQR = Q3 − Q1
3. Définir les bornes :
   - `lower = Q1 - threshold * IQR`
   - `upper = Q3 + threshold * IQR`
4. Clipper les valeurs hors bornes avec `.clip(lower, upper)`

Avec `threshold = 1.5` (règle standard de Tukey), on neutralise les valeurs aberrantes sans supprimer les lignes.

#### Fonction `split_and_scale`

Partitionne les données (`train_test_split`) avec graine fixe, puis normalise via `StandardScaler` si `scale_features: true`.

---

## Partie 3 : Définition des Tests Unitaires

### Objectif

Vérifier automatiquement que le partitionnement est reproductible.

### Fichier `tests/test_preprocessing.py`

Le test `test_split_reproducibility` :

1. Crée un DataFrame fictif de 100 lignes
2. Appelle `split_and_scale` **deux fois** avec la même config (`random_seed: 42`)
3. Compare les matrices avec `np.testing.assert_array_equal`

Si les deux appels produisent des résultats identiques, la graine aléatoire contrôle bien le hasard → reproductibilité garantie.

**Commande :**

```bash
python -m pytest tests/ -v
```

---

## Partie 4 : Gestion du Versionnement Scientifique

### Objectif

Exclure les gros fichiers et caches du dépôt Git tout en préservant l'architecture des dossiers.

### Fichier `.gitignore`

| Règle | Exclusion |
|-------|-----------|
| `__pycache__/`, `*.pyc` | Caches Python |
| `data/raw/*`, `!data/raw/.gitkeep` | Données brutes (garde le dossier vide) |
| `data/processed/*`, `!data/processed/.gitkeep` | Données traitées |
| `.ipynb_checkpoints/` | Checkpoints Jupyter |
| `outputs/` | Résultats générés |
| `.venv/`, `venv/` | Environnements virtuels |

Les fichiers `.gitkeep` permettent de versionner la structure de dossiers sans versionner les données.

**Principe scientifique :** modifier manuellement un fichier de données brutes sans le documenter est une faute de méthode — les données doivent être traçables et immuables dans Git.

---

## Partie 5 : Intégration dans l'Orchestrateur Principal

### Objectif

Point d'entrée unique du pipeline, configurable et exécutable sur serveur.

### Fichier `src/main.py`

1. **Backend Matplotlib `Agg`** — mode non-interactif, indispensable sur serveur/Docker (pas de fenêtre graphique)
2. **Chargement YAML** — `load_config("configs/config.yaml")`
3. **Graine universelle** — `set_seed(config["project"]["random_seed"])`
4. **Pipeline** — chargement CSV → nettoyage → split/scale → logs

```bash
python src/main.py
```

---

## Partie 6 : Stabilité Numérique

### Exercice 6.1 — Sommation naïve vs Kahan

**Fichier :** `exercises/exercise_6_1_sommation.py`

**Problème :** Additionner 1.0 + 10 000 termes de ε/2 en virgule flottante. La somme naïve perd les petits termes (non-associativité IEEE 754).

**Algorithme de Kahan :**
```
y = x - c          # Compense l'erreur précédente
t = somme + y
c = (t - somme) - y  # Erreur d'arrondi accumulée
somme = t
```

**Résultat typique :**
- Somme naïve : `1.0` (les petits termes ignorés)
- Somme Kahan : `1.0000000000011102` (compensation correcte)

---

### Exercice 6.2 — Conditionnement matriciel

**Fichier :** `exercises/exercise_6_2_conditionnement.py`

**Matrice :** Hilbert 3×3 (mal conditionnée)

**Étapes :**
1. `kappa_A = np.linalg.cond(A, 2)` — nombre de conditionnement en norme 2
2. `x_exact = np.linalg.solve(A, b)` — solution exacte (pas d'inversion explicite)
3. Perturbation microscopique : `b[2] += 1e-14`
4. Erreur relative : `||x_exact - x_perturbe|| / ||x_exact||`

**Interprétation :** Si κ(A) ≈ 10¹³ et ε_mach ≈ 10⁻¹⁶, on perd environ log₁₀(κ) ≈ 13 chiffres significatifs. Seuls ~3 chiffres de la solution sont fiables ; le reste est du bruit numérique.

---

### Exercice 6.3 — Inversion explicite vs factorisation directe

**Fichier :** `exercises/exercise_6_3_inversion_vs_solve.py`

**Système :** n = 4000, matrice dense aléatoire

| Approche | Opération | Complexité |
|----------|-----------|------------|
| Mauvaise | `np.linalg.inv(A) @ b` | O(n³) inversion + O(n²) produit |
| Bonne | `np.linalg.solve(A, b)` | O(n³) factorisation LU, pas d'inversion |

**Résultats observés (exemple) :**
- Inversion explicite : ~3.5 s, résidu ~10⁻¹⁰
- Solveur direct : ~1.1 s, résidu ~10⁻¹¹

**Ratio de gain :** ~3× plus rapide avec `solve`, et meilleure précision numérique.

**Justification Flops :** `inv(A)` calcule A⁻¹ entière (n² éléments inutiles), alors que `solve` factorise une fois et résout directement.

---

## Questions de réflexion (Section 8.1)

### 1. Ratio de gain de temps (Exercice 6.3)

Le solveur direct est environ **3× plus rapide** car :
- `inv(A)` : O(2n³/3) pour l'inversion + O(n²) pour le produit matrice-vecteur
- `solve(A, b)` : O(2n³/3) pour la factorisation LU + O(n²) pour les substitutions

L'inversion calcule n colonnes de solutions inutiles ; le solveur ne calcule que la solution demandée.

### 2. Chiffres significatifs perdus

Avec κ(A) = 10¹³ et ε_mach ≈ 10⁻¹⁶ :

Chiffres fiables ≈ 16 − 13 = **3 chiffres significatifs**.

Les autres chiffres du vecteur solution sont du **bruit numérique** — ils semblent précis mais n'ont pas de signification mathématique.

### 3. Éthique et rigueur

Modifier manuellement des données brutes sans documentation :
- Rend impossible la reproductibilité
- Introduit un biais non traçable
- Viole le principe de traçabilité scientifique
- Empêche la vérification par les pairs

---

## Récapitulatif des livrables

| Livrable | Fichier / Dossier |
|----------|-------------------|
| Environnement | `environment.yml` |
| Configuration | `configs/config.yaml` |
| Code source | `src/` |
| Tests | `tests/test_preprocessing.py` |
| Gitignore | `.gitignore` |
| Exercices numériques | `exercises/` |
| Documentation | `DOCUMENTATION.md`, `README.md` |

---

## Commande unique (reproductibilité « un clic »)

```bash
conda activate air_quality_stability
python -m pytest tests/ -v && python src/main.py
```
