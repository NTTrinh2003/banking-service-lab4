from fastapi import FastAPI

from app.agent.orchestrator import run_agent
from app.core.schemas import CustomerRequest, FinalResponse
from app.core.settings import settings

app = FastAPI(title="Banking AI-Agent API Gateway", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def config():
    return {
        "intent_service_target": settings.intent_service_target,
        "ollama_base_url": settings.OLLAMA_BASE_URL,
        "response_model": settings.RESPONSE_MODEL_NAME,
        "intent_confidence_threshold": settings.INTENT_CONFIDENCE_THRESHOLD,
    }


@app.post("/run-agent", response_model=FinalResponse)
def run_agent_endpoint(request: CustomerRequest):
    return run_agent(request.message)
