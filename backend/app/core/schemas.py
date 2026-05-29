from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Intent(str, Enum):
    TRANSFER_FAILURE = "transfer_failure"
    CARD_NOT_RECEIVED = "card_not_received"
    CARD_LOST = "card_lost"
    ACCOUNT_BLOCKED = "account_blocked"
    REFUND_REQUEST = "refund_request"
    BALANCE_INQUIRY = "balance_inquiry"
    SUSPICIOUS_TRANSACTION = "suspicious_transaction"
    GENERAL_INQUIRY = "general_inquiry"
    UNKNOWN = "unknown"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RouterAction(str, Enum):
    SEND_REPLY = "send_reply"
    ASK_FOR_MORE_INFO = "ask_for_more_info"
    ESCALATE_TO_HUMAN = "escalate_to_human"


class IntentResult(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = ""


class PriorityResult(BaseModel):
    priority: Priority
    reason: str


class PolicyResult(BaseModel):
    policy_id: Optional[str] = None
    title: Optional[str] = None
    content: str
    found: bool


class DraftResult(BaseModel):
    draft_reply: str
    missing_information: List[str] = Field(default_factory=list)
    next_action: str


class ValidationResult(BaseModel):
    is_valid: bool
    issues: List[str] = Field(default_factory=list)


class RouterDecision(BaseModel):
    action: RouterAction
    reason: str


class AgentTrace(BaseModel):
    intent: Optional[IntentResult] = None
    priority: Optional[PriorityResult] = None
    policy: Optional[PolicyResult] = None
    draft: Optional[DraftResult] = None
    validation: Optional[ValidationResult] = None
    router: Optional[RouterDecision] = None


class CustomerRequest(BaseModel):
    message: str


class FinalResponse(BaseModel):
    message: str
    final_reply: str
    action: RouterAction
    trace: AgentTrace
