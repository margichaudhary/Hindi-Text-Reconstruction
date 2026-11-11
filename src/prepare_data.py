
from pathlib import Path
import unicodedata
import json
import re

BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(RAW_DIR.glob("*.txt"))

records = []

print("=" * 55)
print("DATA PREPROCESSING")
print("=" * 55)

for file in files:

    # Read original Hindi text
    text = file.read_text(encoding="utf-8")

    # Standardize Unicode representation
    text = unicodedata.normalize("NFC", text)

    # Remove unnecessary leading/trailing whitespace
    text = text.strip()

    # Standardize multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Preserve NULL markers
    words = text.split()

    record = {
        "filename": file.name,
        "text": text,
        "word_count": len(words),
        "character_count": len(text),
        "null_count": words.count("NULL")
    }

    records.append(record)

    print(f"\nFile: {file.name}")
    print(f"Words: {record['word_count']}")
    print(f"Characters: {record['character_count']}")
    print(f"NULL markers: {record['null_count']}")

# Save processed corpus
output_file = OUTPUT_DIR / "corpus.jsonl"

with output_file.open("w", encoding="utf-8") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("\n" + "=" * 55)
print(f"Files processed: {len(records)}")
print(f"Saved to: {output_file}")
print("PREPROCESSING COMPLETED")
print("=" * 55)
