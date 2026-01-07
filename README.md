# RAG Chatbot (Python + Docker + AI)

A Retrieval-Augmented Generation (RAG) chatbot built with **FastAPI** and **Docker**. This project allows you to chat with your own PDF documents using AI.

## 🐳 What is Docker? (And why are we using it?)

If you have ever had the problem where code works on your computer but fails on your friend's computer (missing libraries, different Python versions, etc.), Docker is the solution.

### The Problem
Normally, to run a Python app, you need to:
1. Install Python.
2. Install `pip`.
3. Run `pip install -r requirements.txt`.
4. Hope that your Windows/Mac/Linux versions match exactly.

### The Docker Solution
Docker wraps your application and **everything it needs** (Operating System, Python, Libraries, Code) into a sealed box called a **Container**.

- **Dockerfile**: The "Recipe". It tells Docker how to build the box (e.g., "Start with Linux, install Python, copy my files").
- **Image**: The "Snapshot". This is the built box. You can send this file to anyone (or any server).
- **Container**: The "Running Box". When you click "Run", the image comes alive.

### Why in this project?
1.  **Consistency**: We need specific AI libraries (`langchain`, `chromadb`). Docker ensures you don't mess up your personal PC's Python installation.
2.  **Deployment**: When you are ready to show this to the world, you just give the server your Docker Image. It runs instantly without manual setup.

---

## 🚀 How to Run

### 1. Install & Run Ollama (The Brain)
This project uses a **Local LLM** (TinyLlama) instead of OpenAI to be 100% free and private.
1.  Download [Ollama](https://ollama.com).
2.  Open a terminal and run:
    ```powershell
    ollama run tinyllama
    ```
    (Keep this terminal running or just ensure Ollama is active).

### 2. Build the Docker Image
```bash
docker build -t rag-chatbot .
```

### 3. Ingest Documents (Prepare the Brain)
Before chatting, you need to turn your PDFs into a format the AI can understand (Vectors).
1. Place your PDF files in the `data/` folder.
2. Run the ingestion script inside the Docker container:
   ```bash
   docker run --rm -v ${PWD}/chroma_db:/app/chroma_db -v ${PWD}/data:/app/data rag-chatbot python app/rag.py
   ```
   This will read PDFs from `data/`, convert them, and save the database to `chroma_db/`.

### 4. Run the App
We need to give Docker access to the Ollama server running on your host machine.
```bash
docker run -p 8000:8000 --add-host=host.docker.internal:host-gateway -v ${PWD}/chroma_db:/app/chroma_db rag-chatbot
```

### 5. Interactive API
Go to [http://localhost:8000/docs](http://localhost:8000/docs) to chat with your PDF!

### 6. Usage
- **Status Check**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📂 Project Structure
- `app/`: Contains the actual Python code (`main.py`).
- `data/`: Place your PDF files here (mapped to the container later).
- `Dockerfile`: Instructions for building the container.
- `requirements.txt`: List of Python libraries needed.