"""Exercice 6.2 : Sensibilité au conditionnement."""

import numpy as np

A = np.array([
    [1.0, 1.0 / 2.0, 1.0 / 3.0],
    [1.0 / 2.0, 1.0 / 3.0, 1.0 / 4.0],
    [1.0 / 3.0, 1.0 / 4.0, 1.0 / 5.0],
])

b = np.array([1.0, 0.5, 0.3333])

kappa_A = np.linalg.cond(A, 2)
print(f"Conditionnement kappa(A) = {kappa_A}")

x_exact = np.linalg.solve(A, b)

b_perturbe = b.copy()
b_perturbe[2] += 1e-14

x_perturbe = np.linalg.solve(A, b_perturbe)

erreur_relative = np.linalg.norm(x_exact - x_perturbe) / np.linalg.norm(x_exact)
print(f"Erreur relative sur x : {erreur_relative:.6f}")
