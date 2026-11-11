from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent

input_dir = BASE_DIR / "outputs" / "punctuated"

print("=" * 55)
print("SENTENCE EXTRACTION SUMMARY")
print("=" * 55)

for file_path in sorted(input_dir.glob("sample-*.txt")):

    text = file_path.read_text(encoding="utf-8")

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    word_counts = [len(s.split()) for s in sentences]

    longest = max(word_counts, default=0)

    suspicious = sum(1 for count in word_counts if count > 40)

    print(f"\nFile: {file_path.name}")
    print(f"Sentences extracted: {len(sentences)}")
    print(f"Longest sentence: {longest} words")
    print(f"Suspiciously long sentences: {suspicious}")

print("\nInspection complete!")