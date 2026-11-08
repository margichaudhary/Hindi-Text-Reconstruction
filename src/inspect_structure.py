
from pathlib import Path
import string

DATA_DIR = Path(__file__).parent.parent / "data"

files = sorted(DATA_DIR.glob("*.txt"))

# Punctuation symbols to check
punctuation = set(string.punctuation) | {"।", "॥", "؟", "،"}

print("=" * 65)
print("RAW TEXT STRUCTURE ANALYSIS")
print("=" * 65)

for file in files:

    text = file.read_text(encoding="utf-8")
    words = text.split()

    lines = text.splitlines()

    punctuation_found = [
        char for char in text
        if char in punctuation
    ]

    null_positions = [
        i for i, word in enumerate(words)
        if word == "NULL"
    ]

    consecutive_nulls = sum(
        1 for i in range(len(words) - 1)
        if words[i] == "NULL" and words[i + 1] == "NULL"
    )

    print(f"\nFILE: {file.name}")
    print("-" * 50)

    print("Total lines:", len(lines))
    print("Total words:", len(words))
    print("Existing punctuation:", punctuation_found)
    print("NULL count:", len(null_positions))
    print("Consecutive NULL pairs:", consecutive_nulls)

    if words:
        print("Starts with NULL:", words[0] == "NULL")
        print("Ends with NULL:", words[-1] == "NULL")

    print("\nFirst 200 characters (raw):")
    print(repr(text[:200]))

print("\n" + "=" * 65)
print("ANALYSIS COMPLETED")
print("=" * 65)
