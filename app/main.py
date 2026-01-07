from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

app = FastAPI()

# Input format for the API
class QueryRequest(BaseModel):
    question: str

# 1. Initialize the "Brain" (Vector DB)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
    persist_directory="/app/chroma_db",
    embedding_function=embedding_function
)

# 2. Initialize the "Mouth" (Local Ollama)
# "host.docker.internal" allows Docker to see the Ollama app running on your Windows
# Switching to "tinyllama" because it is much smaller (fits in 1.3GB RAM)
llm = ChatOllama(model="tinyllama", base_url="http://host.docker.internal:11434")

# 3. Connect them (The "RAG" Chain)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3})
)

@app.get("/")
def read_root():
    return {"Status": "RAG Chatbot is Active", "Version": "0.1.0"}

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        # Ask the chain to find data + answer the question
        response = qa_chain.invoke(request.question)
        return {
            "question": request.question,
            "answer": response["result"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))