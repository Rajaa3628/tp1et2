"""Utilitaires de configuration et reproductibilité."""

import random
from pathlib import Path
from typing import Any, Dict

import numpy as np
import yaml


def load_config(config_path: str) -> Dict[str, Any]:
    """Charge un fichier de configuration YAML."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_seed(seed: int) -> None:
    """Fixe les graines aléatoires pour garantir la reproductibilité."""
    random.seed(seed)
    np.random.seed(seed)
