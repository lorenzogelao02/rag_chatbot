from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from app.config import settings
from app.utils import get_vector_store, get_llm

app = FastAPI()

# Input format for the API
class QueryRequest(BaseModel):
    question: str

# 1. Initialize the "Brain" (Vector DB)
db = get_vector_store()
# 2. Initialize the "Mouth" (Local Ollama)
llm = get_llm()

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