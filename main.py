from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.llm.llm_integration import generate_response
from app.vector_db.faiss_integration import store_user_memory

app = FastAPI(title="Cocktail Advisor Chat API")


class QueryRequest(BaseModel):
    question: str

class MemoryRequest(BaseModel):
    content: str

# Check if the message contains phrases indicating that the user is sharing a memory or favorite ingredients/cocktails
def is_user_memory(message: str) -> bool:
    keywords = ["my favorite", "i love", "i enjoy", "i like"]
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in keywords)

@app.post("/query")
async def query_endpoint(query: QueryRequest):
    if is_user_memory(query.question):
        store_user_memory(query.question)
    answer = generate_response(query.question)
    return {"answer": answer}

# Endpoint to store user memories in the vector DB
@app.post("/memory")
async def memory_endpoint(memory: MemoryRequest):
    return {"status": "Memory stored successfully", "content": memory.content}

app.mount("/chat", StaticFiles(directory="app/chat"), name="chat")