from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from app.config import settings

app = FastAPI()

# Input format for the API
class QueryRequest(BaseModel):
    question: str

# 1. Initialize the "Brain" (Vector DB)
embedding_function = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

db = Chroma(
    persist_directory=settings.DB_PATH,
    embedding_function=embedding_function
)

# 2. Initialize the "Mouth" (Local Ollama)
# "host.docker.internal" allows Docker to see the Ollama app running on your Windows
# Switching to "tinyllama" because it is much smaller (fits in 1.3GB RAM)
llm = ChatOllama(model=settings.MODEL_NAME, base_url=settings.OLLAMA_BASE_URL)

# 3. Connect them (The "RAG" Chain)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": settings.RETRIEVAL_K})
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