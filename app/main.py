from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.schema import HumanMessage, SystemMessage
from app.utils import get_llm

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

# 1. Initialize Tools
wiki = WikipediaAPIWrapper()
llm = get_llm()

@app.get("/")
def read_root():
    return {"Status": "Robust Wrapper Bot Active", "Version": "3.0.0"}

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        # Step 1: Search Wikipedia Manually (Python does this, not the AI)
        # This prevents the AI from getting confused or stuck
        print(f"Searching Wikipedia for: {request.question}")
        wiki_results = wiki.run(request.question)
        
        # Step 2: Construct a Prompt with the context
        query = f"""
        Answer the user's question based ONLY on the following context from Wikipedia.
        
        CONTEXT:
        {wiki_results}
        
        QUESTION: 
        {request.question}
        """
        
        # Step 3: Fast Answer
        response = llm.invoke(query)
        
        # Handle the response format (LangChain ChatModel returns a message object)
        answer_text = response.content if hasattr(response, 'content') else str(response)

        return {
            "question": request.question,
            "answer": answer_text,
            "context_found": len(wiki_results) > 0 # Debug info
        }

    except Exception as e:
        return {"error": str(e)}