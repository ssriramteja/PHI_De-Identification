# PHI De-identification Pipeline

A modular, hybrid pipeline for detecting and masking Protected Health Information (PHI) in clinical documentation. This system integrates high-precision regular expressions with spaCy Named Entity Recognition (NER) to provide a robust de-identification solution.

## Key Features

- **Hybrid Detection Engine**: Combines deterministic rule-based matching (for structured data like MRNs, dates, and emails) with transformer-compatible NER (for unstructured data like names and clinical locations).
- **Flexible Masking Strategies**: Supports generic tag masking (`[LABEL]`) and pseudonymization via surrogate generation (`[LABEL_001]`).
- **Extensible Architecture**: Decoupled modules for rules, models, and merging logic allow for easy integration of clinical-specific models (e.g., ScispaCy).
- **Control Interface**: Includes both a professional CLI for batch processing and a Streamlit-based dashboard for real-time validation.

## Project Structure

```text
phi-deidentification-pipeline/
├── src/
│   ├── rules.py         # Regex-based PHI detectors
│   ├── ner_model.py     # spaCy NER wrapper with label mapping
│   ├── merger.py        # Span conflict resolution and masking logic
│   ├── pipeline.py      # Core orchestration class
│   └── cli.py           # CLI entry point
├── ui/
│   └── app.py           # Streamlit dashboard
├── tests/
│   └── test_phi_pipeline.py # Unit test suite
├── data/
│   └── synthetic_notes.txt  # Sample testing dataset
├── requirements.txt
└── README.md
```

## Setup and Usage

### Prerequisites
- Python 3.9+
- Virtual environment recommended

### Installation
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Running the CLI Demo
```bash
# Basic usage
python src/cli.py

# Verbose mode with custom text
python src/cli.py --verbose --text "Patient Jane Doe presented on 2024-05-01."
```

### Running the Dashboard
```bash
streamlit run ui/app.py
```

### Running the Test Suite
```bash
pytest tests/
```

---
*Disclaimer: This tool is intended for research and development. It must be validated against specific institutional compliance and privacy standards before any production use.*

