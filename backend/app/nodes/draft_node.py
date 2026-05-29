from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftResult, IntentResult, PolicyResult, PriorityResult
from app.core.settings import settings

_client = OllamaClient(base_url=settings.OLLAMA_BASE_URL, timeout=settings.OLLAMA_TIMEOUT)

_SYSTEM_PROMPT = (
    "You are a helpful bank customer-support assistant. Using the provided intent, "
    "priority, and policy, write a concise, professional reply to the customer. "
    "Respond ONLY as JSON: "
    '{"draft_reply": "<text>", "missing_information": ["<item>", ...], '
    '"next_action": "<what the agent should do next>"}.'
)


def run(
    message: str,
    intent: IntentResult,
    priority: PriorityResult,
    policy: PolicyResult,
) -> DraftResult:
    user_prompt = (
        f"Customer message: {message}\n"
        f"Detected intent: {intent.intent.value} (confidence {intent.confidence:.2f})\n"
        f"Priority: {priority.priority.value} ({priority.reason})\n"
        f"Relevant policy: {policy.content}\n\n"
        "Write the reply now."
    )

    try:
        raw = _client.generate_json(
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=settings.RESPONSE_MODEL_NAME,
        )
        missing = raw.get("missing_information", [])
        if isinstance(missing, str):
            missing = [missing]
        return DraftResult(
            draft_reply=str(raw.get("draft_reply", "")),
            missing_information=[str(m) for m in missing],
            next_action=str(raw.get("next_action", "review")),
        )
    except Exception as exc:
        # Fallback so the pipeline still returns a result if Ollama is unreachable.
        return DraftResult(
            draft_reply="We are reviewing your request and will get back to you shortly.",
            missing_information=[],
            next_action=f"manual_review (draft generation failed: {exc})",
        )
