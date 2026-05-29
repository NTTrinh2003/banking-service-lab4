from app.clients.grpc_intent_client import GrpcIntentClient
from app.core.schemas import Intent, IntentResult

_client = GrpcIntentClient()


def run(message: str) -> IntentResult:
    raw_intent, confidence, reason = _client.recognize(message)
    try:
        intent = Intent(raw_intent)
    except ValueError:
        intent = Intent.UNKNOWN
    return IntentResult(intent=intent, confidence=confidence, reason=reason)
