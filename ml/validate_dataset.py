from pathlib import Path
import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "binary_dataset.csv"
)


def main():
    print("=" * 70)
    print("BINARY DATASET VALIDATION")
    print("=" * 70)

    print(f"\nDataset: {DATASET_FILE}")

    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    df = pd.read_csv(
        DATASET_FILE,
        low_memory=False
    )

    print("\nBasic information")
    print("-" * 70)
    print(f"Rows       : {len(df):,}")
    print(f"Columns    : {len(df.columns):,}")

    print("\nRequired columns")
    print("-" * 70)
    print(f"Label exists        : {'Label' in df.columns}")
    print(f"Binary_Label exists : {'Binary_Label' in df.columns}")

    print("\nBinary label distribution")
    print("-" * 70)
    print(df["Binary_Label"].value_counts().sort_index())

    print("\nBinary label percentages")
    print("-" * 70)
    print(
        df["Binary_Label"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(3)
    )

    print("\nMissing values")
    print("-" * 70)
    missing = df.isna().sum()
    missing_total = int(missing.sum())

    print(f"Total missing values: {missing_total:,}")

    if missing_total > 0:
        print("\nColumns containing missing values:")
        print(
            missing[missing > 0]
            .sort_values(ascending=False)
        )

    print("\nInfinite values")
    print("-" * 70)

    numeric_df = df.select_dtypes(include=[np.number])
    infinite_count = int(
        np.isinf(numeric_df.to_numpy()).sum()
    )

    print(f"Total infinite values: {infinite_count:,}")

    print("\nOriginal attack labels")
    print("-" * 70)
    print(
        df["Label"]
        .value_counts()
        .head(20)
    )

    print("\nData types")
    print("-" * 70)
    print(df.dtypes.value_counts())

    print("\nValidation complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()