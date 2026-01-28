from datasets import load_dataset
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.config import settings
from app.utils import get_embedding_function

def ingest_dataset():
    print("Connecting to Hugging Face (Wikipedia)...")
    
    # 1. Stream the dataset (Don't download the whole thing!)
    # We use "20220301.simple" which is Simple English Wikipedia
    dataset = load_dataset("wikipedia", "20220301.simple", split="train", streaming=True)
    
    docs = []
    count = 0
    MAX_DOCS = 50  # Limit to 50 articles for speed/lightweight

    print(f"Downloading and processing the first {MAX_DOCS} articles...")
    
    for entry in dataset:
        if count >= MAX_DOCS:
            break
            
        # Extract fields
        text = entry['text']
        title = entry['title']
        url = entry['url']
        
        # Create LangChain Document
        # We attach the URL so the bot can tell you the source!
        doc = Document(
            page_content=text,
            metadata={"source": url, "title": title}
        )
        docs.append(doc)
        print(f"   -> Added: {title}")
        count += 1

    # 2. Chunking (Same as before)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Split {count} articles into {len(chunks)} chunks.")

    # 3. Store in DB
    embedding_function = get_embedding_function()
    
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=settings.DB_PATH
    )
    print("Success! Dataset embedded to ChromaDB.")

if __name__ == "__main__":
    ingest_dataset()