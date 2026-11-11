
from pathlib import Path
import json

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


# Project paths
BASE_DIR = Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "models" / "punctuation"

MODEL_PATH = MODEL_DIR / "onnx" / "model_quantized.onnx"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"
CONFIG_PATH = MODEL_DIR / "config.json"


# Load tokenizer and label mapping
tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))

config = json.loads(
    CONFIG_PATH.read_text(encoding="utf-8")
)

id2label = {
    int(key): value
    for key, value in config["id2label"].items()
}


# Load ONNX model on CPU
session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

MAX_LENGTH = 8192


def restore_punctuation(text):

    text = text.strip()

    if not text:
        return text

    # Tokenize Hindi text
    encoding = tokenizer.encode(text)

    if len(encoding.ids) > MAX_LENGTH:
        raise ValueError(
            f"Input has {len(encoding.ids)} tokens. "
            "Split the text into smaller chunks first."
        )

    input_ids = np.array(
        [encoding.ids], dtype=np.int64
    )

    attention_mask = np.ones_like(
        input_ids, dtype=np.int64
    )

    # Run ONNX inference
    logits = session.run(
        ["logits"],
        {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }
    )[0][0]

    predictions = np.argmax(logits, axis=-1)

    # Identify the final subword of every word
    word_groups = []
    current_group = []

    for i, token in enumerate(encoding.tokens):

        # Ignore special tokens
        if token in ("<bos>", "<eos>"):
            continue

        # SentencePiece marker indicates a new word
        if token.startswith("▁") and current_group:
            word_groups.append(current_group)
            current_group = []

        current_group.append(i)

    if current_group:
        word_groups.append(current_group)

    # Insert predicted punctuation at word boundaries
    insertions = []

    for group in word_groups:

        last_token_index = group[-1]

        label_id = int(predictions[last_token_index])
        punctuation = id2label[label_id]

        if punctuation != "0":

            end_position = encoding.offsets[last_token_index][1]

            if end_position > 0:
                insertions.append(
                    (end_position, punctuation)
                )

    # Reconstruct text
    result = text

    for position, punctuation in sorted(
        insertions, reverse=True
    ):
        result = (
            result[:position]
            + punctuation
            + result[position:]
        )

    return result


if __name__ == "__main__":

    input_dir = BASE_DIR / "data" / "raw"
    output_dir = BASE_DIR / "outputs" / "punctuated"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Process all seven sample files
    for sample_path in sorted(input_dir.glob("sample-*.txt")):

        original_text = sample_path.read_text(
            encoding="utf-8"
        )

        # Split text into chunks of 150 words
        words = original_text.split()

        chunk_size = 150

        chunks = [
            words[i:i + chunk_size]
            for i in range(0, len(words), chunk_size)
        ]

        restored_chunks = []

        # Restore punctuation in each chunk
        for chunk in chunks:

            chunk_text = " ".join(chunk)

            restored_chunks.append(
                restore_punctuation(chunk_text)
            )

        # Combine restored chunks
        result = " ".join(restored_chunks)

        # Save output
        output_path = output_dir / sample_path.name

        output_path.write_text(
            result,
            encoding="utf-8"
        )

        print(f"Processed: {sample_path.name}")
        print(f"Saved: {output_path}")

    print("\nAll samples processed!")
