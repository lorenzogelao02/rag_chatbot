from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, AgentType
from app.utils import get_llm

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

# 1. Initialize the Tool (The "Hands")
# This wrapper handles searching and summarizing Wiki pages
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# 2. Initialize the Brain (Ollama)
llm = get_llm()

# 3. Create the Agent (Brain + Hands)
agent_executor = initialize_agent(
    tools=[wikipedia], 
    llm=llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # Logs thoughts to console (helpful for debugging)
    handle_parsing_errors=True
)

@app.get("/")
def read_root():
    return {"Status": "Wikipedia Agent is Active", "Version": "2.0.0"}

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        # The agent decides strictly what to do
        response = agent_executor.invoke(request.question)
        return {
            "question": request.question,
            "answer": response["output"]
        }
    except Exception as e:
        # If the agent gets confused or fails
        return {"question": request.question, "answer": f"Error: {str(e)}"}