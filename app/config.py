import os

class Settings:
    #1. Paths
    # os.getenv to allow overriding via .env file or Docker env vars
    DATA_PATH = os.getenv("DATA_PATH", "/app/data")
    DB_PATH = os.getenv("DB_PATH", "/app/chroma_db")

    #2. Models
    #Changable 
    MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")

    # Emedding model for converting text to vectors
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # 3. RAG Parameters
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", 3)) # Number of documents to retrieve
    
    # 4. Infrastructure
    # host.docker.internal is needed for Docker to talk to Ollama on Windows
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

    # Instantiate setting so It can be imported
    setting = Settings()