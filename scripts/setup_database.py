from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.database.database import init_database


def main():
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)

    init_database()

    print("\nDatabase initialized successfully.")
    print("Database: data/security.db")


if __name__ == "__main__":
    main()