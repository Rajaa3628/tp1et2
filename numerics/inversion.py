"""Exercice 6.3 : Inversion explicite vs factorisation directe."""

import numpy as np
import time

n = 4000
rng = np.random.RandomState(42)
A = rng.rand(n, n)
b = rng.rand(n)

t0 = time.time()
x_inv = np.linalg.inv(A) @ b
t_inv = time.time() - t0
residu_inv = np.linalg.norm(A @ x_inv - b)

t0 = time.time()
x_solve = np.linalg.solve(A, b)
t_solve = time.time() - t0
residu_solve = np.linalg.norm(A @ x_solve - b)

print(f"Inversion Explicite -> Temps: {t_inv:.4f}s | Residu: {residu_inv}")
print(f"Solveur Direct     -> Temps: {t_solve:.4f}s | Residu: {residu_solve}")
