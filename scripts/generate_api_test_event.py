from pathlib import Path
import json

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "binary_dataset.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "scripts"
    / "test_event.json"
)


def main():
    print("=" * 70)
    print("GENERATING API TEST EVENT")
    print("=" * 70)

    df = pd.read_csv(
        DATASET_FILE,
        nrows=1,
        low_memory=False,
    )

    feature_columns = [
        column
        for column in df.columns
        if column not in {
            "Label",
            "Binary_Label",
        }
    ]

    event = {
        "features": {
            column: df.iloc[0][column].item()
            if hasattr(df.iloc[0][column], "item")
            else df.iloc[0][column]
            for column in feature_columns
        }
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            event,
            file,
            indent=2,
        )

    print(f"\nGenerated event with {len(feature_columns)} features.")
    print(f"Output: {OUTPUT_FILE}")

    print("\nOriginal dataset label:")
    print(df.iloc[0]["Label"])

    print("\nBinary label:")
    print(df.iloc[0]["Binary_Label"])


if __name__ == "__main__":
    main()