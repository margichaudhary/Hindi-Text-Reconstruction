# Hindi Text Reconstruction

A Natural Language Processing (NLP) project that processes unstructured Hindi text by restoring punctuation, estimating sentence order, grouping sentences, and translating the reconstructed text into English.

## Project Overview

The project processes seven Hindi text samples containing unpunctuated and jumbled sentences.

The pipeline consists of four major stages:

1. **Text Preprocessing:** Normalize Hindi text, clean whitespace, and preserve NULL markers.
2. **Punctuation Restoration:** Use a pretrained multilingual punctuation restoration model to restore punctuation.
3. **Sentence Ordering and Grouping:** Apply TF-IDF and cosine similarity to estimate sentence order, then group sentences into sets of five.
4. **Translation:** Translate the grouped Hindi text into English using AI4Bharat's IndicTrans2 model.

## Technologies Used

- Python
- ONNX Runtime
- Tokenizers
- Scikit-learn
- TF-IDF and Cosine Similarity
- Hugging Face Transformers
- IndicTrans2
- Jupyter Notebook
- Google Colab

## Project Structure

```text
Hindi-Text-Reconstruction/
│
├── data/
│   ├── raw/
│   │   ├── sample-1.txt
│   │   ├── sample-2.txt
│   │   └── ... sample-7.txt
│   └── processed/
│       └── corpus.jsonl
│
├── models/
│   └── punctuation/
│       ├── config.json
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       └── special_tokens_map.json
│
├── notebooks/
│   └── indictrans2_translation.ipynb
│
├── src/
│   ├── inspect_data.py
│   ├── inspect_nulls.py
│   ├── inspect_structure.py
│   ├── prepare_data.py
│   ├── inspect_corpus.py
│   ├── inspect_sentences.py
│   ├── punctuate.py
│   ├── sentence_ordering.py
│   └── group_sentences.py
│
├── outputs/
│   ├── punctuated/
│   ├── ordered/
│   ├── grouped/
│   └── translated/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Processing Pipeline

### 1. Data Inspection and Preprocessing

- Inspected the seven Hindi text files.
- Analyzed NULL markers and the structure of the raw text.
- Applied Unicode NFC normalization.
- Normalized whitespace while preserving NULL markers.
- Stored the processed corpus in JSONL format.

### 2. Punctuation Restoration

- Used the `Horizon-Labs/punctuation-restoration-small` multilingual model.
- Ran inference using ONNX Runtime on CPU.
- Processed text in smaller chunks to handle long inputs.
- Restored punctuation such as full stops, commas, question marks, hyphens, and colons.

### 3. Sentence Ordering

- Used TF-IDF vectorization to represent sentences.
- Calculated cosine similarity between sentence representations.
- Applied a greedy nearest-neighbour approach to estimate a possible sentence sequence.

### 4. Sentence Grouping

- Grouped the ordered sentences into sets of five.
- Preserved all sentences.
- The final group may contain fewer than five sentences.

### 5. English Translation

- Used AI4Bharat's `indictrans2-indic-en-dist-200M` model.
- Performed translation using Google Colab.
- Used CPU inference to avoid GPU memory requirements.
- Saved the translated outputs for all seven samples.

## Jupyter Notebook

The `notebooks/` directory contains the Jupyter notebook used for the Hindi-to-English translation stage.

**`indictrans2_translation.ipynb`**

- Contains the IndicTrans2 model setup and initialization.
- Implements batch translation of grouped Hindi text into English.
- Demonstrates the translation workflow using Google Colab.

The remaining stages of the project, including preprocessing, punctuation restoration, sentence ordering, and grouping, are implemented separately using Python scripts in the `src/` directory.

## Dataset Summary

| Metric | Result |
|---|---:|
| Input files | 7 |
| Total words | 5,821 |
| NULL markers | 67 |
| Punctuated segments | 368 |
| Sentence groups | 76 |

## Models Used

**Punctuation Restoration:**  
[Horizon-Labs/punctuation-restoration-small](https://huggingface.co/Horizon-Labs/punctuation-restoration-small)

**Hindi-to-English Translation:**  
[AI4Bharat IndicTrans2](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M)

Both models are pretrained models used for inference. No models were trained from scratch or fine-tuned.

The ONNX model binary is excluded from this repository because of its large file size. The required model file must be obtained separately and placed in the expected model directory before running punctuation restoration.

## Installation

Clone the repository:

```bash
git clone https://github.com/margichaudhary/Hindi-Text-Reconstruction.git
cd Hindi-Text-Reconstruction
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Important Notes

- Translation was performed
