"""Exercice 6.2 : Le Multiplicateur de Mensonge — Sensibilite au conditionnement."""

import numpy as np

# Generation d'une matrice mal conditionnee (Matrice de Hilbert modifiee)
A = np.array([
    [1.0, 1.0 / 2.0, 1.0 / 3.0],
    [1.0 / 2.0, 1.0 / 3.0, 1.0 / 4.0],
    [1.0 / 3.0, 1.0 / 4.0, 1.0 / 5.0],
])

b = np.array([1.0, 0.5, 0.3333])

# 1. Calcul du conditionnement
kappa_A = np.linalg.cond(A, 2)

print(f"Conditionnement de la matrice de resolution kappa(A) = {kappa_A}")

# 2. Resolution du systeme exact
x_exact = np.linalg.solve(A, b)

# 3. Injection d'une perturbation microscopique sur le vecteur b
b_perturbe = b.copy()
b_perturbe[2] += 1e-14

# Resolution du systeme avec perturbation
x_perturbe = np.linalg.solve(A, b_perturbe)

# 4. Calcul de l'erreur relative sur la solution finale
erreur_relative = np.linalg.norm(x_exact - x_perturbe) / np.linalg.norm(x_exact)
print(f"Erreur relative induite sur la prediction x : {erreur_relative:.6f}")
