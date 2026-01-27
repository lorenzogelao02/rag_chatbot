# 🤖 RAG Chatbot (Python + Docker + AI)

A Retrieval-Augmented Generation (RAG) chatbot built with **FastAPI** and **Docker**. This project allows you to chat with your own PDF documents using a local AI (Ollama).

---

## 🚀 Quick Start Guide

### 1. Prerequisites
You need the following installed:
1.  **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
2.  **Ollama** ([Download](https://ollama.com/)) - To run the AI model.

### 2. Prepare the AI Model
Open a terminal and download the model (we use `tinyllama` for speed/efficiency):
```powershell
ollama pull tinyllama
```
*Keep Ollama running in the background.*

### 3. Build the Application
Open your terminal in the project folder and build the Docker image:
```powershell
docker build -t rag-bot .
```

### 4. Ingest Your Documents (The "Brain")
Place your PDF files inside the `data/` folder. Then, run the ingestion script to create the vector database:

```powershell
docker run --rm -v ${PWD}/data:/app/data -v ${PWD}/chroma_db:/app/chroma_db rag-bot python -m app.rag
```
*   This reads PDFs from your local `data/` folder.
*   It saves the "memory" to your local `chroma_db/` folder so it persists.

### 5. Run the Chatbot
Start the API server:
```powershell
docker run -p 8000:8000 -v ${PWD}/chroma_db:/app/chroma_db rag-bot
```
You should see: `Uvicorn running on http://0.0.0.0:8000`.

---

## 🧪 How to Use

### Interactive Interface (Swagger UI)
Go to: [http://localhost:8000/docs](http://localhost:8000/docs)
1.  Click **POST /chat**.
2.  Click **Try it out**.
3.  Enter your question in the JSON body:
    ```json
    {
      "question": "What does the CV say about the user?"
    }
    ```
4.  Click **Execute**.

### Project Structure
*   `app/config.py`: Central configuration (Paths, Model names).
*   `app/rag.py`: Script to ingest PDFs and create the vector database.
*   `app/main.py`: The API server (FastAPI).
*   `app/utils.py`: Helper functions for Database and AI connections.
*   `data/`: Folder for your input PDFs.
*   `chroma_db/`: Folder where the Vector Database is saved.