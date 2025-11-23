# Named Entity Recognition (NER) Development

A comprehensive Named Entity Recognition system for Indonesian text, featuring baseline model comparison and fine-tuning capabilities using XLM-RoBERTa.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Baseline Experiment](#baseline-experiment)
  - [Fine-Tuning Pipeline](#fine-tuning-pipeline)
  - [Model Inference](#model-inference)
- [Models](#models)
- [Data Format](#data-format)
- [Configuration](#configuration)
- [Evaluation Metrics](#evaluation-metrics)
- [Results](#results)
- [Utilities](#utilities)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project provides a complete pipeline for Named Entity Recognition (NER) in Indonesian language texts. The system supports three main entity types:

- **PER**: Person names
- **ORG**: Organization names
- **LOC**: Location names

The project includes baseline model comparison capabilities and a complete fine-tuning pipeline using XLM-RoBERTa (Cross-lingual Language Model - RoBERTa) with progressive training support.

## Features

- **Multiple Model Support**: Compare performance across different pre-trained NER models
- **Fine-Tuning Pipeline**: Complete training workflow with XLM-RoBERTa
- **Label Studio Integration**: Support for Label Studio format annotations
- **Comprehensive Evaluation**: Precision, recall, F1-score, and accuracy metrics
- **GPU Optimization**: Automatic GPU detection and utilization
- **Progressive Training**: Iterative fine-tuning with incremental data
- **Model Persistence**: Save and load trained models from Google Drive or local storage
- **Flexible Configuration**: Easy-to-modify configuration parameters

## Project Structure

```
NER Development/
├── main.ipynb                          # Main notebook with all experiments
├── Input/                              # Input data directory
│   └── 1000 berita 2025_json.json     # Training data in JSON format
├── service/                            # Utility scripts
│   ├── csv_to_labelstudio.py          # CSV to Label Studio format converter
│   └── elastic_fetch.ipynb            # Elasticsearch data fetching utilities
├── .env.example                        # Example environment variables
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## Installation

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for training)
- Google Colab account (optional, for cloud training)

### Dependencies

Install required packages:

```bash
pip install transformers datasets seqeval evaluate accelerate pandas numpy tqdm
```

For GPU support:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "NER Development"
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Configure your environment variables in `.env`

## Usage

### Baseline Experiment

The baseline experiment compares multiple pre-trained NER models on Indonesian text.

**Supported Models:**

1. **cahya/bert-base-indonesian-NER**: BERT-based model trained on Indonesian NER
2. **Davlan/xlm-roberta-base-ner-hrl**: Multilingual XLM-RoBERTa for high-resource languages
3. **flair/ner-indonesian-large**: Flair NER model for Indonesian


### Fine-Tuning Pipeline

The fine-tuning pipeline allows you to train a custom NER model on your annotated data.

**Step 1: Configuration**

```python
JSON_PATH = "/path/to/your/data.json"
BASE_MODEL = "Davlan/xlm-roberta-base-ner-hrl"
MODEL_SAVE_NAME = "xlmr_finetuned_ner_custom"
```

**Step 2: Load and Prepare Data**

```python
# Data is automatically loaded and converted to BIO format
bio_data = create_bio_format_labelstudio(data)
```

**Step 3: Tokenization**

```python
# Tokenization with label alignment
tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)
```

**Step 4: Training**

```python
trainer.train()
```

**Step 5: Evaluation**

```python
results = trainer.evaluate()
print(f"F1 Score: {results['eval_f1']:.4f}")
print(f"Precision: {results['eval_precision']:.4f}")
print(f"Recall: {results['eval_recall']:.4f}")
```

**Step 6: Save Model**

```python
SAVE_PATH = "/path/to/save/model"
trainer.save_model(SAVE_PATH)
```

### Model Inference

**Load Fine-Tuned Model:**

```python
model_path = "/path/to/saved/model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

ner_pipeline = pipeline(
    "token-classification",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)
```

**Predict Entities:**

```python
text = "HOLOPIS.COM, JAKARTA – Menteri Pemuda dan Olahraga Dito Ariotedjo..."
entities = predict_entities(text)

for entity in entities:
    print(f"{entity['entity']}: {entity['word']} (confidence: {entity['score']})")
```

## Models

### Base Models

| Model | Type | Language | Parameters |
|-------|------|----------|------------|
| cahya/bert-base-indonesian-NER | BERT | Indonesian | 125M |
| Davlan/xlm-roberta-base-ner-hrl | XLM-RoBERTa | Multilingual | 270M |
| flair/ner-indonesian-large | Flair | Indonesian | - |

## Data Format

### Label Studio JSON Format

```json
[
  {
    "data": {
      "summary": "Text content here..."
    },
    "annotations": [
      {
        "result": [
          {
            "value": {
              "start": 0,
              "end": 10,
              "labels": ["PER"]
            }
          }
        ]
      }
    ]
  }
]
```

### BIO Format

The system internally converts Label Studio format to BIO (Beginning, Inside, Outside) tagging:

- **B-PER**: Beginning of person entity
- **I-PER**: Inside person entity
- **B-ORG**: Beginning of organization entity
- **I-ORG**: Inside organization entity
- **B-LOC**: Beginning of location entity
- **I-LOC**: Inside location entity
- **O**: Outside any entity

## Configuration

### Training Arguments

```python
TrainingArguments(
    output_dir="./model_output",
    eval_strategy="epoch",           # Evaluate every epoch
    save_strategy="epoch",            # Save checkpoint every epoch
    learning_rate=2e-5,               # Learning rate
    per_device_train_batch_size=4,   # Batch size for training
    per_device_eval_batch_size=4,    # Batch size for evaluation
    num_train_epochs=4,               # Number of training epochs
    weight_decay=0.01,                # Weight decay for regularization
    logging_steps=20,                 # Log every N steps
    push_to_hub=False,                # Don't push to HuggingFace Hub
)
```

### Model Configuration

```python
MODEL_REGISTRY = {
    "xlmr": {
        "type": "hf",
        "model": "Davlan/xlm-roberta-base-ner-hrl",
        "tokenizer": "Davlan/xlm-roberta-base-ner-hrl"
    }
}
```

## Evaluation Metrics

The system computes the following metrics using seqeval:

- **Precision**: Proportion of predicted entities that are correct
- **Recall**: Proportion of actual entities that are correctly identified
- **F1-Score**: Harmonic mean of precision and recall
- **Accuracy**: Token-level accuracy

### Interpretation

- **High Precision, Low Recall**: Model is conservative, misses many entities
- **Low Precision, High Recall**: Model is aggressive, makes false predictions
- **High F1-Score**: Good balance between precision and recall


## Utilities

### CSV to Label Studio Converter

Convert CSV files with ground truth annotations to Label Studio JSON format:

```python
from service.csv_to_labelstudio import convert_to_ls_format

# Configure input/output
NAMA_FILE_CSV = "data.csv"
NAMA_FILE_JSON_OUTPUT = "data_berlabel.json"

# Run conversion
df = pd.read_csv(NAMA_FILE_CSV)
convert_to_ls_format(df)
```

**Required CSV Columns:**
- `summary`: Text content
- `gt_PER`: List of person entities
- `gt_LOC`: List of location entities
- `gt_ORG`: List of organization entities

## License

This project is licensed under the MIT License - see the LICENSE file for details.