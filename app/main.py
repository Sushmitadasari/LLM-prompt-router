from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse
from .classifier import classify_intent
from .router import route_and_respond
from .logger import log_route

app = FastAPI(title="LLM Prompt Router")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    intent_data = classify_intent(request.message)

    intent = intent_data["intent"]
    confidence = intent_data["confidence"]

    final_response = route_and_respond(request.message, intent_data)

    log_route(intent, confidence, request.message, final_response)

    return ChatResponse(
        intent=intent,
        confidence=confidence,
        response=final_response
    )