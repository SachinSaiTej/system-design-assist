# System Design Assistant (Local)

A local-first, research-capable system design aide with diagrams.

## Features
- Local LLM via **Ollama** or **llama.cpp**
- RAG with **ChromaDB** and **SentenceTransformers**
- Web research via DuckDuckGo (optional)
- Mermaid diagram output
- Runs locally with **Streamlit**

---

## Quickstart

### 1️⃣ Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
