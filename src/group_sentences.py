
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent

INPUT_DIR = BASE_DIR / "outputs" / "ordered"
OUTPUT_DIR = BASE_DIR / "outputs" / "grouped"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def group_sentences(sentences, group_size=5):
    """Divide sentences into groups of five."""

    groups = []

    for i in range(0, len(sentences), group_size):
        group = sentences[i:i + group_size]
        groups.append(group)

    return groups


if __name__ == "__main__":

    files = sorted(INPUT_DIR.glob("sample-*.txt"))

    for file_path in files:

        print(f"\nProcessing: {file_path.name}")

        # Read ordered sentences
        text = file_path.read_text(encoding="utf-8")

        sentences = [
            sentence.strip()
            for sentence in text.splitlines()
            if sentence.strip()
        ]

        # Create groups of five
        groups = group_sentences(sentences)

        # Prepare output
        output_text = []

        for i, group in enumerate(groups, start=1):

            output_text.append(f"GROUP {i}")

            for sentence in group:
                output_text.append(sentence)

            output_text.append("")

        # Save grouped sentences
        output_path = OUTPUT_DIR / file_path.name

        output_path.write_text(
            "\n".join(output_text),
            encoding="utf-8"
        )

        print(f"Total sentences: {len(sentences)}")
        print(f"Total groups: {len(groups)}")
        print(f"Saved: {output_path}")

    print("\nAll files grouped successfully!")
