from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent / "data" / "raw"

CHUNK_SIZE = 100_000


def analyze_file(file_path: Path) -> None:
    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    label_counts = {}
    total_rows = 0
    total_missing = 0

    try:
        for chunk in pd.read_csv(
            file_path,
            chunksize=CHUNK_SIZE,
            low_memory=False
        ):
            chunk.columns = chunk.columns.str.strip()

            total_rows += len(chunk)

            # Count labels
            counts = (
                chunk["Label"]
                .astype(str)
                .str.strip()
                .value_counts()
            )

            for label, count in counts.items():
                label_counts[label] = (
                    label_counts.get(label, 0) + int(count)
                )

            # Count missing values
            total_missing += int(chunk.isna().sum().sum())

        print(f"Total rows: {total_rows:,}")

        print("\nLabel distribution:")

        for label, count in sorted(
            label_counts.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            percentage = (count / total_rows) * 100

            print(
                f"  {label:<30} "
                f"{count:>12,} "
                f"({percentage:>7.3f}%)"
            )

        print(f"\nTotal missing values: {total_missing:,}")

    except Exception as exc:
        print(f"ERROR: {exc}")


def main() -> None:

    files = sorted(DATA_DIR.glob("*.csv"))

    if not files:
        print("No CSV files found.")
        return

    print(f"Found {len(files)} CSV files.")

    for file_path in files:
        analyze_file(file_path)


if __name__ == "__main__":
    main()