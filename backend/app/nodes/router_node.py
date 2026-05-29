from app.core.schemas import (
    Priority,
    PriorityResult,
    RouterAction,
    RouterDecision,
    ValidationResult,
)


def run(priority: PriorityResult, validation: ValidationResult) -> RouterDecision:
    if priority.priority == Priority.HIGH:
        return RouterDecision(
            action=RouterAction.ESCALATE_TO_HUMAN,
            reason=f"high priority -> human handling ({priority.reason})",
        )

    if not validation.is_valid:
        return RouterDecision(
            action=RouterAction.ASK_FOR_MORE_INFO,
            reason=f"validation issues: {', '.join(validation.issues)}",
        )

    return RouterDecision(
        action=RouterAction.SEND_REPLY,
        reason="passed validation and not high priority",
    )
