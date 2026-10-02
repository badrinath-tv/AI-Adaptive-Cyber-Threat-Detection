from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent / "data" / "raw"


def inspect_file(file_path: Path) -> None:
    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    try:
        # Read only a small sample first
        df = pd.read_csv(
            file_path,
            nrows=1000,
            low_memory=False
        )

        # Remove accidental whitespace from column names
        df.columns = df.columns.str.strip()

        print(f"Sample rows       : {len(df):,}")
        print(f"Columns           : {len(df.columns)}")

        print("\nColumn names:")
        for i, column in enumerate(df.columns, start=1):
            print(f"  {i:2}. {column}")

        print("\nData types:")
        print(df.dtypes.to_string())

        print("\nMissing values in sample:")
        missing = df.isna().sum()
        missing = missing[missing > 0]

        if missing.empty:
            print("  No missing values found in sample.")
        else:
            print(missing.to_string())

        # Look for the CICIDS label column
        label_candidates = [
            column
            for column in df.columns
            if column.lower() in {
                "label",
                "class",
                "target"
            }
        ]

        if label_candidates:
            print("\nPotential label column(s):")
            for column in label_candidates:
                print(f"  {column}")

                print("\nLabel distribution in sample:")
                print(
                    df[column]
                    .astype(str)
                    .str.strip()
                    .value_counts()
                    .to_string()
                )
        else:
            print("\nNo obvious label column found.")

    except Exception as exc:
        print(f"\nERROR: {exc}")


def main() -> None:
    files = sorted(DATA_DIR.glob("*.csv"))

    if not files:
        print(f"No CSV files found in: {DATA_DIR}")
        return

    print(f"Dataset directory: {DATA_DIR}")
    print(f"CSV files found  : {len(files)}")

    for file_path in files:
        inspect_file(file_path)


if __name__ == "__main__":
    main()