"""Point d'entrée unique du pipeline."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from app.utils import load_config, set_seed
from app.preprocessing import clean_data, split_and_scale
import pandas as pd


def main():
    config = load_config("settings/config.yaml")
    set_seed(config["project"]["random_seed"])

    print("[RUN] Execution du pipeline scientifique ...")

    data_path = Path(config["data"]["path"])
    if data_path.exists():
        df = pd.read_csv(data_path)
        df_clean = clean_data(df, config)
        X_train, X_test, y_train, y_test, _ = split_and_scale(df_clean, config)
        print(f"[OK] Donnees chargees : {len(df)} lignes")
        print(f"[OK] Train : {X_train.shape[0]} | Test : {X_test.shape[0]}")
    else:
        print(f"[WARN] Fichier de donnees absent : {data_path}")

    output_dir = Path(config["project"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Pipeline termine. Sorties dans : {output_dir}")


if __name__ == "__main__":
    main()
