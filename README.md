# Faithful Concept Mapper: BRSR Faithfulness Audit

An AI-powered system that audits corporate Business Responsibility and Sustainability Reports (BRSR) for faithfulness against SEBI mandates. This project primarily focuses on **Principle 6 (Environmental Responsibilities)**.

## 🚀 Features

*   **Ingestion Engine (`src/ingest.py`)**: Loads complex PDFs, preserves page numbers, and chunks text for analysis.
*   **Structued Extraction**: Uses OpenAI GPT-4o (via LangChain) to extract specific metrics (Emissions Sc 1/2, Water Intensity, Waste) into a strict Pydantic Schema.
*   **Verification Engine (`src/eval.py`)**: A "Veritas-style" evaluation module that calculates **Drift Scores (0-3)** by comparing extracted claims against SEBI requirements using local BERT models (`nli-deberta-v3-small`).
*   **Automated Reporting (`src/report.py`)**: Generates a professional Word document (`.docx`) with the audit findings.

## 🛠️ Tech Stack

*   **Language**: Python 3.10+
*   **AI/LLM**: OpenAI GPT-4o, Sentence Transformers (Local BERT)
*   **Orchestration**: LangChain
*   **Vector Query**: ChromaDB (Ready for RAG expansion)
*   **Validation**: Pydantic V2
*   **Visualization**: Plotly (Sankey Diagrams)

## 📂 Project Structure

```
├── data/                   # Input PDFs (e.g., target_report.pdf)
├── output/                 # Generated Deliverables (Word Report)
├── src/
│   ├── ingest.py           # PDF Ingestion & Extraction Logic
│   ├── eval.py             # Evaluation & Drift Calculation
│   ├── schema.py           # Pydantic Models (Principle 6)
│   └── report.py           # Word Report Generator
├── notebooks/
│   ├── 01_ingest.ipynb     # Interactive Extraction Demo
│   └── 02_analysis.ipynb   # Full Pipeline Analysis & Visualization
├── requirements.txt        # Dependencies
└── .env                    # API Keys and Config
```

## ⚡ How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    Create a `.env` file with your OpenAI Key:
    ```
    OPENAI_API_KEY=sk-proj-...
    ```

3.  **Run Analysis (Interactive)**:
    Open `notebooks/02_analysis.ipynb` and Run All cells.

4.  **Generate Report (Automated)**:
    Run the reporter script to get the Word doc:
    ```bash
    python src/report.py
    ```
    Find the report in `output/Faithfulness_Audit_Report.docx`.

## 📊 Methodology

1.  **Extraction Strategy**: Used a "DataWeave-inspired" agentic approach where specific schemas enforce data quality (preventing hallucinated units).
2.  **Metric Calculation**:
    *   **Drift Score 0**: Entailment (High confidence match).
    *   **Drift Score 2**: Neutral (Data present but abstract).
    *   **Drift Score 3**: Contradiction (Data missing or hallucinated).

## 📄 License
Academic / Portfolio Use.
