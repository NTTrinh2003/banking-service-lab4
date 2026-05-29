from typing import Dict

# Small in-memory policy lookup keyed by intent.
POLICIES: Dict[str, dict] = {
    "transfer_failure": {
        "policy_id": "POL-001",
        "title": "Failed Transfer Handling",
        "content": (
            "If a transfer fails, funds are auto-reversed within 1-3 business days. "
            "Ask the customer for the transaction reference and the date of the attempt."
        ),
    },
    "card_not_received": {
        "policy_id": "POL-002",
        "title": "Card Delivery",
        "content": (
            "New cards are delivered within 7-10 business days. After 10 days a "
            "replacement can be issued. Verify the customer's registered address."
        ),
    },
    "card_lost": {
        "policy_id": "POL-003",
        "title": "Lost or Stolen Card",
        "content": (
            "Immediately block a lost/stolen card to prevent fraud, then issue a "
            "replacement. This is a high-priority security action."
        ),
    },
    "account_blocked": {
        "policy_id": "POL-004",
        "title": "Account Unblocking",
        "content": (
            "Accounts are blocked after suspicious activity or repeated failed logins. "
            "Identity verification is required before unblocking."
        ),
    },
    "refund_request": {
        "policy_id": "POL-005",
        "title": "Refunds",
        "content": (
            "Refunds for disputed charges are processed within 5-7 business days "
            "after the dispute is validated. Collect the transaction details."
        ),
    },
    "balance_inquiry": {
        "policy_id": "POL-006",
        "title": "Balance Inquiries",
        "content": (
            "Balances can be checked in-app or at an ATM. Never disclose a balance "
            "without verifying the customer's identity."
        ),
    },
    "suspicious_transaction": {
        "policy_id": "POL-007",
        "title": "Suspicious Activity",
        "content": (
            "Flag suspicious transactions, freeze the affected card, and escalate to "
            "the fraud team. Treat as high priority."
        ),
    },
}


def get_policy(intent: str) -> dict | None:
    return POLICIES.get(intent)
