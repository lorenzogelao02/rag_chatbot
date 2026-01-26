from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from app.config import settings

def get_embedding_function():
    """Calculates and returns the embedding function based on config."""
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

def get_vector_store():
    """Initializes and returns the ChromaDB connection."""
    return Chroma(
        persist_directory=settings.DB_PATH,
        embedding_function=get_embedding_function()
    )

def get_llm():
    return ChatOllama(
        model = settings.MODEL_NAME,
        base_url = settings.OLLAMA_BASE_URL
    )