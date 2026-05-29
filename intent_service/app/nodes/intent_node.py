from app.clients.ollama_client import OllamaClient
from app.core.schemas import INTENT_LABELS, IntentPrediction
from app.core.settings import settings

_client = OllamaClient(base_url=settings.OLLAMA_BASE_URL, timeout=settings.OLLAMA_TIMEOUT)

_SYSTEM_PROMPT = (
    "You are an intent classifier for a bank's customer support system. "
    "You must classify each customer message into exactly one intent label "
    f"from this fixed list: {', '.join(INTENT_LABELS)}. "
    "Respond ONLY with a JSON object of the form "
    '{"intent": "<label>", "confidence": <0..1 float>, "reason": "<short reason>"}. '
    "Use \"unknown\" if the message does not clearly fit any label."
)


def predict_intent(message: str) -> IntentPrediction:
    user_prompt = f"Customer message: {message}"

    try:
        raw = _client.chat_json(
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=settings.INTENT_MODEL_NAME,
        )
        intent = str(raw.get("intent", "unknown")).strip().lower()
        if intent not in INTENT_LABELS:
            intent = "unknown"
        confidence = float(raw.get("confidence", 0.0))
        confidence = max(0.0, min(1.0, confidence))
        reason = str(raw.get("reason", ""))[:300]
        return IntentPrediction(intent=intent, confidence=confidence, reason=reason)
    except Exception as exc:
        return IntentPrediction(
            intent="unknown",
            confidence=0.0,
            reason=f"intent classification failed: {exc}",
        )
