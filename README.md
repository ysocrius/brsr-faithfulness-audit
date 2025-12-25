# BRSR Faithfulness Audit

An AI-powered system for auditing corporate Business Responsibility and Sustainability Reports (BRSR) against SEBI Principle 6 (Environmental Responsibilities). This project ensures compliance by detecting "drift" between reported disclosures and regulatory mandates.

## 🎯 Overview

This system audits how faithfully companies report their environmental metrics (Emissions, Water, Waste) by:
1. **Extracting** structured data from BRSR PDFs using GPT-4o
2. **Evaluating** faithfulness using local NLI models (drift scoring 0-3)
3. **Visualizing** evidence flows with Sankey diagrams
4. **Generating** automated audit reports with color-coded dashboards

## 📊 Sankey Diagram: Evidence Flow

![BRSR Audit Flow](output/newplot.png)

*Visualization showing the flow from SEBI Requirements → Company Disclosures → Drift Scores*

## ✨ Key Features

- **🔍 Structured Extraction**: Pydantic V2 schemas enforce strict data types (no hallucinations)
- **📏 Drift Evaluation**: 0-3 scale using NLI cross-encoders (nli-deberta-v3-small)
- **📝 Automated Reporting**: Generates Word documents with color-coded drift dashboards
- **🎨 Interactive Visualizations**: Sankey diagrams for evidence flow analysis
- **🔗 Citation Support**: Links claims to source text with page numbers
- **🚫 Non-Hallucination Proof**: Evidence-based justification for each metric

## 🏗️ Architecture

**Hybrid RAG Approach:**
- **DataWeave**: Structured extraction with AI agents
- **Veritas**: Groundedness evaluation using NLI models
- **CalQuity**: Citation engine with page-level metadata

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **AI/LLM**: OpenAI GPT-4o, Sentence Transformers
- **Orchestration**: LangChain
- **Vector DB**: ChromaDB (ready for RAG expansion)
- **Validation**: Pydantic V2
- **Visualization**: Plotly
- **Reporting**: python-docx

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/ysocrius/brsr-faithfulness-audit.git
cd brsr-faithfulness-audit

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OpenAI API key to .env
```

### Usage

**Option 1: Interactive Analysis (Recommended)**
```bash
jupyter notebook notebooks/02_analysis.ipynb
```

**Option 2: Generate Report Directly**
```bash
python -m src.report
```

Output will be saved to `output/BRSR_Faithfulness_Audit_SUBMISSION.docx`

## 📂 Project Structure

```
├── data/                   # Input PDFs
├── output/                 # Generated reports and visualizations
├── src/
│   ├── ingest.py          # PDF ingestion & extraction
│   ├── eval.py            # Drift evaluation engine
│   ├── schema.py          # Pydantic models (Principle 6)
│   └── report.py          # Word report generator
├── notebooks/
│   ├── 01_ingest.ipynb    # Extraction demo
│   └── 02_analysis.ipynb  # Full pipeline + Sankey diagram
└── requirements.txt
```

## 📋 Deliverables

- ✅ **Drift Scores**: 0 (Verbatim) to 3 (Hallucinated/Missing)
- ✅ **Citations**: Page-level evidence from source documents
- ✅ **Non-Hallucination Justification**: Evidence-based rationale
- ✅ **Sankey Diagram**: Visual evidence flow
- ✅ **Color-Coded Dashboard**: Green/Orange/Red drift indicators

## 🎓 AI/RAG Concepts Employed

1. **Structured Extraction**: Schema enforcement via Pydantic V2
2. **RAG Chunking**: RecursiveCharacterTextSplitter with page metadata
3. **NLI Evaluation**: Zero-shot classification for groundedness
4. **Drift Detection**: Cross-encoder models for entailment scoring

## 📄 License

Academic / Portfolio Use

## 🙏 Acknowledgments

- SEBI for BRSR framework
- Reference projects: Veritas Pipeline, DataWeave TurerZ, CalQuity AI Chat
