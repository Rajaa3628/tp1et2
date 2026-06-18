"""Exercice 6.3 : Inversion Explicite vs Factorisation Directe."""

import numpy as np
import time

# Generation d'un systeme lineaire dense de grande taille
n = 4000
rng = np.random.RandomState(42)
A = rng.rand(n, n)
b = rng.rand(n)

# --- Approche A : Mauvaise pratique (Inversion explicite) ---
t0 = time.time()
x_inv = np.linalg.inv(A) @ b
t_inv = time.time() - t0
residu_inv = np.linalg.norm(A @ x_inv - b)

# --- Approche B : Bonne pratique (Factorisation stable) ---
t0 = time.time()
x_solve = np.linalg.solve(A, b)
t_solve = time.time() - t0
residu_solve = np.linalg.norm(A @ x_solve - b)

print(f"Inversion Explicite -> Temps: {t_inv:.4f}s | Norme du residu: {residu_inv}")
print(f"Solveur Direct -> Temps: {t_solve:.4f}s | Norme du residu: {residu_solve}")
