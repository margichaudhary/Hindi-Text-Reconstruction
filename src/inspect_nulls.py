
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

files = sorted(DATA_DIR.glob("*.txt"))

print("=" * 65)
print("INVESTIGATING NULL MARKERS")
print("=" * 65)

total_nulls = 0

for file in files:

    text = file.read_text(encoding="utf-8")
    words = text.split()

    null_positions = [
        i for i, word in enumerate(words)
        if word == "NULL"
    ]

    print(f"\nFILE: {file.name}")
    print(f"Total NULL markers: {len(null_positions)}")

    total_nulls += len(null_positions)

    for position in null_positions:

        start = max(0, position - 3)
        end = min(len(words), position + 4)

        context = words[start:end]

        print("\nContext:")
        print(" ".join(context))

print("\n" + "=" * 65)
print(f"TOTAL NULL MARKERS: {total_nulls}")
print("INVESTIGATION COMPLETED")
print("=" * 65)
