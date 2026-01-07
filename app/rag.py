import os  
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# This directory will hold the "database" file locally
DB_PATH = "/app/chroma_db"
DATA_PATH = "/app/data"

def ingest_documents():
    """
    Reads PDF from /app/data, splits them and adds them to the Vector DB
    """
    #1. Load  Data
    if not os.path.exists(DATA_PATH):
        print(f"Warning: {DATA_PATH} does not exist.")
        return

    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDFs.")

    #2. Split Text (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split pages into {len(chunks)} small chunks.")

    #3. Add to Vector DB 
    # Switch to Local Embeddings (Free, runs on CPU)
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    #Create or update the DB
    Chroma.from_documents(
        documents = chunks,
        embedding = embedding_function,
        persist_directory = DB_PATH
    )

    print("Success! Documents embedded and saved to ChromaDB.")
if __name__ == "__main__":
    # This allows us to run this file directly to train the model
    ingest_documents()
    

    