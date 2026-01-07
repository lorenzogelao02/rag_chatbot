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

### 1. Build the "Box" (Image)
This creates the Docker image based on our `Dockerfile`.
```bash
docker build -t rag-chatbot .
```

### 2. Run the App
This starts the container and forwards port 8000 from the container to port 8000 on your PC.
```bash
docker run -p 8000:8000 rag-chatbot
```

### 3. Usage
- **Status Check**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📂 Project Structure
- `app/`: Contains the actual Python code (`main.py`).
- `data/`: Place your PDF files here (mapped to the container later).
- `Dockerfile`: Instructions for building the container.
- `requirements.txt`: List of Python libraries needed.