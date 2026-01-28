# 🤖 RAG Chatbot (PDFs + Wikipedia Agent)

A smart chatbot built with **FastAPI**, **Docker**, and **Ollama**.
It has two powerful modes:
1.  **Chat with Docs**: Read and answer questions from your local PDF files.
2.  **Chat with Wikipedia**: Live search Wikipedia to answer general questions.

---

## 🚀 Quick Start

### 1. Prerequisites
1.  **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
2.  **Ollama** ([Download](https://ollama.com/))

### 2. Prepare the AI
Open a terminal and pull the lightweight model:
```powershell
ollama pull tinyllama
```

### 3. Build & Run
Build the container:
```powershell
docker build -t rag-bot .
```

Run the bot (Agent Mode):
```powershell
docker run -p 8000:8000 --add-host=host.docker.internal:host-gateway rag-bot
```
Go to **[http://localhost:8000/docs](http://localhost:8000/docs)** and start chatting!

---

## 🧠 Advanced Usage

### Mode A: Ingest Local PDFs
To chat with your own files (e.g., CVs, Manuals):
1.  Put PDF files in `data/`.
2.  Run the ingestion script:
    ```powershell
    docker run --rm -v ${PWD}/data:/app/data -v ${PWD}/chroma_db:/app/chroma_db rag-bot python -m app.rag
    ```
    *This creates a local "Brain" in the `chroma_db` folder.*

### Mode B: Ingest Wikipedia Dataset
To build a knowledge base from random Wikipedia articles (Streaming):
```powershell
docker run --rm -v ${PWD}/chroma_db:/app/chroma_db rag-bot python -m app.ingest_dataset
```

---

## ⚙️ Configuration
You can change settings in `app/config.py` or by passing Environment Variables to Docker:
-   `MODEL_NAME`: Change to `mistral` or `gemma:2b` for smarter answers.
-   `CHUNK_SIZE`: Adjust how text is split.

## 📂 Project Structure
*   `app/main.py`: The API Agent (Decides to search Wiki or answer directly).
*   `app/rag.py`: Script to ingest PDFs.
*   `app/ingest_dataset.py`: Utility to stream datasets from HuggingFace.
*   `app/config.py`: Central settings.