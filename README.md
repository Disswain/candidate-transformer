# Candidate Data Transformer

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()


A production-style ETL pipeline that extracts, normalizes, validates, merges, and projects candidate information from multiple heterogeneous sources into a single canonical candidate profile - complete with confidence scoring and field-level provenance tracking.

---

## Table of Contents

- [Why This Exists](#why-this-exists)
- [Features](#features)
- [Pipeline Architecture](#pipeline-architecture)
- [Project Structure](#project-structure)
- [Source Priority](#source-priority)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [Sample Output](#sample-output)
- [Configuration](#configuration)
- [Design Decisions](#design-decisions)
- [Assumptions](#assumptions)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Why This Exists

Recruitment systems pull candidate data from a patchwork of sources — recruiter spreadsheets, ATS exports, LinkedIn, GitHub, and resumes in half a dozen formats. Every source has its own structure, its own quirks, and its own blind spots. This project takes that mess and turns it into one clean, validated, deduplicated JSON profile per candidate — with full traceability back to where every field came from.

---

## Features

**Multi-source extraction**
- Recruiter CSV
- ATS JSON
- LinkedIn Profile
- GitHub Profile
- Resume (TXT)
- Resume (PDF)

**Normalization**
- Names · Emails · Phone numbers (E.164) · Countries (ISO-3166) · Skills · Dates · URLs

**Merging & deduplication**
- Configurable source-priority resolution
- Deduplicates emails, phone numbers, skills, experience, and education entries

**Trust & traceability**
- Per-field confidence scoring
- Full provenance tracking for every extracted value

**Output**
- Schema-validated canonical profile
- Configurable JSON projection
- Automated unit test suite

---

## Pipeline Architecture

```
Input Sources
      │
      ▼
  Extractors          (source-specific parsing)
      │
      ▼
IntermediateCandidate  (raw, unnormalized representation)
      │
      ▼
  Normalization        (formats, units, casing)
      │
      ▼
Canonical Candidate
      │
      ▼
  Validation           (schema + business rules)
      │
      ▼
  Merge Resolver        (source-priority conflict resolution)
      │
      ▼
Confidence Calculator
      │
      ▼
  Projection Layer      (configurable output schema)
      │
      ▼
  Output JSON
```

Each stage has a single responsibility, which keeps extraction, normalization, merging, and output formatting independently testable and swappable.

---

## Project Structure

```
candidate-transformer/
│
├── config/
│   └── default.json
│
├── sample_data/
│   ├── structured/
│   └── unstructured/
│
├── outputs/
│
├── src/
│   ├── extractors/
│   ├── merge/
│   ├── models/
│   ├── normalizers/
│   ├── projection/
│   ├── validation/
│   ├── utils/
│   └── pipeline.py
│
├── tests/
│
├── requirements.txt
├── design.pdf
└── README.md
```

---

## Source Priority

When the same field appears in multiple sources, the merge resolver picks a value using this priority order (configurable in `config/default.json`):

| Priority | Source         |
|----------|----------------|
| 1        | Recruiter CSV  |
| 2        | ATS JSON       |
| 3        | LinkedIn       |
| 4        | GitHub         |
| 5        | Resume PDF     |
| 6        | Resume TXT     |

---

## Technologies Used

| Library          | Purpose                          |
|-------------------|-----------------------------------|
| `pydantic`        | Data modeling & validation       |
| `rapidfuzz`       | Fuzzy matching for deduplication |
| `phonenumbers`    | Phone number parsing/E.164       |
| `python-dateutil` | Flexible date parsing            |
| `pycountry`       | Country code normalization       |
| `pytest`          | Testing framework                |


Compatible with **Python 3.11+** (tested with Python 3.13).

---

## Installation

```bash
git clone https://github.com/Disswain/candidate-transformer.git
cd candidate-transformer

python -m venv .venv
```

**Windows**

```powershell
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

## CLI Help

Display all available command-line options:

```bash
python -m src.main --help
```

Example output:

```
usage: candidate-transformer [-h]
                             --input INPUT
                             --config CONFIG
                             --output OUTPUT

options:
  -h, --help         show this help message and exit
  --input INPUT      Directory containing input candidate files
  --config CONFIG    Path to configuration JSON
  --output OUTPUT    Output JSON file path
```

```bash
python -m src.main --input sample_data --config config/default.json --output outputs/result.json
```

| Flag       | Description                                  |
|------------|-----------------------------------------------|
| `--input`  | Directory containing source candidate files   |
| `--config` | Path to pipeline configuration JSON           |
| `--output` | Destination path for the canonical output JSON|

---

## Running Tests

```bash
pytest
```

```
==========================
8 passed in 2.7s
==========================
```

The project contains automated unit tests covering:

- Phone normalization
- Email normalization
- Name normalization
- Skill normalization
- Date normalization
- Merge resolver
- Projection layer
- End-to-end pipeline execution

---

## Sample Output

```json
{
  "candidate_id": "C001",
  "full_name": "John Anderson",
  "emails": [
    "john.anderson@example.com"
  ],
  "phones": [
    "+14155551234"
  ],
  "location": {
    "city": "San Francisco",
    "region": "California",
    "country": "US"
  }
}
```

The generated output also includes normalized skills, experience, education, confidence scores, and field-level provenance.

---

## Configuration

All transformation behavior is driven by `config/default.json`, including:

- Source priority order
- Confidence weight tuning per source/field
- Which fields appear in the final projected output
- Behavior when a field is missing across all sources
- Normalization rules (e.g. date formats, phone region defaults)

---

## Design Decisions

- **Intermediate data model** isolates raw extraction from normalization logic.
- **Single-responsibility normalizers** — one normalizer, one concern (e.g. just phone numbers).
- **Merge logic is decoupled from extraction**, so new sources don't require touching the resolver.
- **Configurable projection layer** lets consumers request only the fields they need.
- **Confidence and provenance are computed post-merge**, once the final value per field is known.
- **Modular architecture** — new extractors or normalizers can be added with minimal changes elsewhere.

---

## Assumptions

- All input files in a given run belong to the same candidate.
- Recruiter CSV is treated as the most reliable source.
- Phone numbers are normalized to E.164 format.
- Countries are normalized to ISO-3166 Alpha-2 codes.
- Duplicate skills are merged case-insensitively.
- Invalid emails and phone numbers are dropped rather than blocking the pipeline.

---

## Future Improvements

- [ ] OCR support for scanned resumes
- [ ] Entity resolution across multiple candidates
- [ ] Machine learning–based confidence scoring
- [ ] REST API interface
- [ ] Database persistence layer
- [ ] Parallelized extraction pipeline

---

## Author

**Disita Swain**
B.Tech Computer Science & Engineering (Cybersecurity)
SOA University