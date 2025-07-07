#Step1: setup pydantic model
from aiohttp import request
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    prompt: str
    messages: List[str]
    allow_search: bool
    #Step2: setup AI agent from frontend request

from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAME= ["llama-3.3-70b-versatile", "gpt-4o-mini"]
app = FastAPI(title="langgraph AI Agent")
@app.post("/chat")
def chat_endpoint(request:RequestState):
    """
   API Endpoint to interact with the Chatbot using langgraph and search tools.
   It dynamically selects the model specified in the request 
    """
    if request.model_name not in ALLOWED_MODEL_NAME: 
       return {"error": "Invalid model name. Kindly select a valid AI model"}
#create ai agent and get response from it. 
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    prompt = request.prompt
    provider = request.model_provider

    response = get_response_from_ai_agent(llm_id, query, allow_search, prompt, provider)
    return response
#step 3: run and explore swagger ui docs.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
