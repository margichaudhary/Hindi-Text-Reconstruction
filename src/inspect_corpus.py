
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CORPUS_FILE = BASE_DIR / "data" / "processed" / "corpus.jsonl"

with CORPUS_FILE.open("r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f]

print("CORPUS VERIFICATION")
print("=" * 45)

for record in records:

    words = record["text"].split()

    null_positions = [
        i for i, word in enumerate(words)
        if word == "NULL"
    ]

    print(f"\n{record['filename']}")
    print("Words:", len(words))
    print("NULL positions:", null_positions)

print("\nTotal records:", len(records))
print("Verification completed!")
