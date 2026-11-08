
from pathlib import Path

# Locate the data folder
DATA_DIR = Path(__file__).parent.parent / "data"

# Find all text files
files = sorted(DATA_DIR.glob("*.txt"))

print("=" * 50)
print("HINDI DATASET ANALYSIS")
print("=" * 50)

print(f"\nTotal files found: {len(files)}")

for file in files:

    # Read the file
    text = file.read_text(encoding="utf-8")

    # Basic statistics
    words = text.split()
    null_count = text.count("NULL")

    print("\n" + "-" * 50)
    print(f"File: {file.name}")
    print(f"Characters: {len(text)}")
    print(f"Words: {len(words)}")
    print(f"NULL markers: {null_count}")

    print("\nFirst 300 characters:")
    print(text[:300])

print("\n" + "=" * 50)
print("DATASET ANALYSIS COMPLETED")
print("=" * 50)
