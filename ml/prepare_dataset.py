from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "ml" / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "binary_dataset.csv"


# ============================================================
# Configuration
# ============================================================

CHUNK_SIZE = 100_000
LABEL_COLUMN = "Label"


# ============================================================
# Utility functions
# ============================================================

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


def clean_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if LABEL_COLUMN not in df.columns:
        raise ValueError(
            f"'{LABEL_COLUMN}' column not found."
        )

    df[LABEL_COLUMN] = (
        df[LABEL_COLUMN]
        .astype(str)
        .str.strip()
    )

    return df


def convert_features_to_numeric(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    feature_columns = [
        column
        for column in df.columns
        if column != LABEL_COLUMN
    ]

    for column in feature_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


def clean_numeric_values(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    numeric_columns = df.select_dtypes(
        include=[np.number]
    ).columns

    df[numeric_columns] = (
        df[numeric_columns]
        .replace([np.inf, -np.inf], np.nan)
    )

    return df


def create_binary_label(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["Binary_Label"] = (
        df[LABEL_COLUMN]
        .str.upper()
        .ne("BENIGN")
        .astype("int8")
    )

    return df


# ============================================================
# First pass
# ============================================================

def calculate_global_means(
    files: list[Path],
) -> dict[str, float]:

    print("\nCalculating global numeric means...")

    sums: dict[str, float] = {}
    counts: dict[str, int] = {}

    feature_columns = None

    for file_path in files:

        print(f"  Reading: {file_path.name}")

        for chunk in pd.read_csv(
            file_path,
            chunksize=CHUNK_SIZE,
            low_memory=False,
        ):

            chunk = clean_columns(chunk)
            chunk = clean_labels(chunk)
            chunk = convert_features_to_numeric(chunk)
            chunk = clean_numeric_values(chunk)

            if feature_columns is None:

                feature_columns = [
                    column
                    for column in chunk.columns
                    if column != LABEL_COLUMN
                ]

                for column in feature_columns:
                    sums[column] = 0.0
                    counts[column] = 0

            for column in feature_columns:

                values = chunk[column].dropna()

                if values.empty:
                    continue

                sums[column] += float(
                    values.sum()
                )

                counts[column] += len(values)

    means = {}

    for column in feature_columns:

        if counts[column] == 0:
            means[column] = 0.0
        else:
            means[column] = (
                sums[column] / counts[column]
            )

    return means


# ============================================================
# Process one chunk
# ============================================================

def process_chunk(
    chunk: pd.DataFrame,
    fill_values: dict[str, float],
) -> pd.DataFrame:

    chunk = clean_columns(chunk)
    chunk = clean_labels(chunk)

    # Convert all network features to numeric
    chunk = convert_features_to_numeric(chunk)

    # Replace +/- infinity
    chunk = clean_numeric_values(chunk)

    # Remove rows with invalid labels
    chunk = chunk[
        chunk[LABEL_COLUMN].notna()
    ].copy()

    # Create binary target
    chunk = create_binary_label(chunk)

    feature_columns = [
        column
        for column in chunk.columns
        if column not in {
            LABEL_COLUMN,
            "Binary_Label",
        }
    ]

    # Fill missing numeric values
    for column in feature_columns:

        chunk[column] = (
            chunk[column]
            .fillna(fill_values[column])
        )

    # Remove duplicates inside the chunk
    chunk = chunk.drop_duplicates()

    return chunk


# ============================================================
# Process complete dataset
# ============================================================

def process_dataset(
    files: list[Path],
    fill_values: dict[str, float],
) -> None:

    if OUTPUT_FILE.exists():
        print(
            f"\nDeleting existing output:"
            f"\n{OUTPUT_FILE}"
        )

        OUTPUT_FILE.unlink()

    first_write = True

    total_rows = 0
    benign_rows = 0
    attack_rows = 0

    for file_path in files:

        print("\n" + "=" * 70)
        print(f"Processing {file_path.name}")
        print("=" * 70)

        for chunk_number, chunk in enumerate(
            pd.read_csv(
                file_path,
                chunksize=CHUNK_SIZE,
                low_memory=False,
            ),
            start=1,
        ):

            processed = process_chunk(
                chunk,
                fill_values,
            )

            if processed.empty:
                continue

            processed.to_csv(
                OUTPUT_FILE,
                mode="w" if first_write else "a",
                header=first_write,
                index=False,
            )

            first_write = False

            rows = len(processed)

            total_rows += rows

            benign_rows += int(
                (
                    processed["Binary_Label"] == 0
                ).sum()
            )

            attack_rows += int(
                (
                    processed["Binary_Label"] == 1
                ).sum()
            )

            print(
                f"Chunk {chunk_number:>3}: "
                f"{rows:,} rows"
            )

    print("\n" + "=" * 70)
    print("PREPROCESSING COMPLETE")
    print("=" * 70)

    print(f"Output file : {OUTPUT_FILE}")
    print(f"Total rows  : {total_rows:,}")
    print(f"BENIGN      : {benign_rows:,}")
    print(f"ATTACK      : {attack_rows:,}")

    if total_rows:

        print(
            f"BENIGN %    : "
            f"{benign_rows / total_rows * 100:.3f}%"
        )

        print(
            f"ATTACK %    : "
            f"{attack_rows / total_rows * 100:.3f}%"
        )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("CICIDS2017 DATA PREPARATION")
    print("=" * 70)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = sorted(
        RAW_DIR.glob("*.csv")
    )

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DIR}"
        )

    print(
        f"\nFound {len(files)} CSV files."
    )

    for file_path in files:
        print(
            f"  {file_path.name}"
        )

    # First pass
    fill_values = calculate_global_means(
        files
    )

    print(
        f"\nCalculated fill values for "
        f"{len(fill_values)} features."
    )

    # Second pass
    process_dataset(
        files,
        fill_values,
    )


if __name__ == "__main__":
    main()