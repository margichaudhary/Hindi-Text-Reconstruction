
from pathlib import Path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Project paths
BASE_DIR = Path(__file__).parent.parent

INPUT_DIR = BASE_DIR / "outputs" / "punctuated"
OUTPUT_DIR = BASE_DIR / "outputs" / "ordered"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_sentences(text):
    """Split text into individual sentences."""

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def order_sentences(sentences):
    """Arrange sentences using TF-IDF cosine similarity."""

    if len(sentences) <= 1:
        return sentences

    # Convert sentences into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        token_pattern=r"(?u)\b\w+\b"
    )

    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Calculate pairwise cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Find the least-connected sentence as the starting point
    max_similarities = similarity_matrix.copy()

    # Ignore self-similarity
    for i in range(len(sentences)):
        max_similarities[i][i] = 0

    start_index = min(
        range(len(sentences)),
        key=lambda i: max_similarities[i].max()
    )

    # Greedy nearest-neighbour ordering
    ordered_indices = [start_index]
    remaining = set(range(len(sentences)))
    remaining.remove(start_index)

    while remaining:

        current_index = ordered_indices[-1]

        next_index = max(
            remaining,
            key=lambda i: similarity_matrix[current_index][i]
        )

        ordered_indices.append(next_index)
        remaining.remove(next_index)

    return [sentences[i] for i in ordered_indices]


if __name__ == "__main__":

    for file_path in sorted(INPUT_DIR.glob("sample-*.txt")):

        print(f"\nProcessing: {file_path.name}")

        text = file_path.read_text(encoding="utf-8")

        # Extract sentences
        sentences = extract_sentences(text)

        # Arrange sentences
        ordered = order_sentences(sentences)

        # Save ordered sentences
        output_path = OUTPUT_DIR / file_path.name

        output_path.write_text(
            "\n".join(ordered),
            encoding="utf-8"
        )

        print(f"Original sentences: {len(sentences)}")
        print(f"Ordered sentences: {len(ordered)}")
        print(f"Saved to: {output_path}")

    print("\nAll files processed!")
