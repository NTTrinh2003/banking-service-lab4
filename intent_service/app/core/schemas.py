from typing import List

from pydantic import BaseModel, Field

INTENT_LABELS: List[str] = [
    "transfer_failure",
    "card_not_received",
    "card_lost",
    "account_blocked",
    "refund_request",
    "balance_inquiry",
    "suspicious_transaction",
    "general_inquiry",
    "unknown",
]


class IntentPrediction(BaseModel):
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
