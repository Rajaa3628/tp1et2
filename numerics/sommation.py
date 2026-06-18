"""Exercice 6.1 : Sommation naïve vs Kahan."""

import numpy as np


def sommation_naive(tableau):
    somme = 0.0
    for x in tableau:
        somme += x
    return somme


def sommation_kahan(tableau):
    somme = 0.0
    c = 0.0
    for x in tableau:
        y = x - c
        t = somme + y
        c = (t - somme) - y
        somme = t
    return somme


if __name__ == "__main__":
    epsilon_machine = np.finfo(float).eps
    print(f"Epsilon Machine : {epsilon_machine}")

    valeurs = [1.0] + [epsilon_machine / 2.0] * 10000

    print(f"Somme Naive : {sommation_naive(valeurs)}")
    print(f"Somme Kahan : {sommation_kahan(valeurs)}")
