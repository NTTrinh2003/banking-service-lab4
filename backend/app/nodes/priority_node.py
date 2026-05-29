from app.core.schemas import Intent, Priority, PriorityResult

_HIGH_INTENTS = {Intent.CARD_LOST, Intent.SUSPICIOUS_TRANSACTION, Intent.ACCOUNT_BLOCKED}
_HIGH_KEYWORDS = ("fraud", "stolen", "hacked", "unauthorized", "urgent", "emergency")
_MEDIUM_KEYWORDS = ("failed", "blocked", "cannot", "can't", "missing", "wrong")


def run(message: str, intent: Intent) -> PriorityResult:
    text = message.lower()

    if intent in _HIGH_INTENTS:
        return PriorityResult(priority=Priority.HIGH, reason=f"high-risk intent: {intent.value}")

    for kw in _HIGH_KEYWORDS:
        if kw in text:
            return PriorityResult(priority=Priority.HIGH, reason=f"matched high keyword: '{kw}'")

    for kw in _MEDIUM_KEYWORDS:
        if kw in text:
            return PriorityResult(priority=Priority.MEDIUM, reason=f"matched medium keyword: '{kw}'")

    return PriorityResult(priority=Priority.LOW, reason="no risk indicators found")
