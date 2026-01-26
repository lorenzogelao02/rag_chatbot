import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

DATA_PATH = "/app/data"       # Directory containing your PDFs
DB_PATH = "/app/chroma_db"    # Directory for the vector database

def ingest_documents():
    # 1. Load Data
    if not os.path.exists(settings.DATA_PATH):
        print(f"Warning: {settings.DATA_PATH} does not exist.")
        return

    loader = PyPDFDirectoryLoader(settings.DATA_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDFs.")

    # 2. Split Text (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=setting.CHUNK_SIZE,      # Characters per chunk
        chunk_overlap=setting.CHUNK_OVERLAP   # Overlap to keep context between chunks
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split pages into {len(chunks)} small chunks.")

    # 3. Add to Vector DB
    # We use the same model as in main.py to ensuring matching "language"
    embedding_function = HuggingFaceEmbeddings(model_name=setting.EMBEDDING_MODEL)

    # Save to disk
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=settings.DB_PATH
    )
    print("Success! Documents embedded and saved to ChromaDB.")

if __name__ == "__main__":
    ingest_documents()