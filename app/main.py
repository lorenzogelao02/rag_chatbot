from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "RAG Chatbot is Active", "Version": "0.1.0"}