from app.core.schemas import DraftResult, IntentResult, ValidationResult
from app.core.settings import settings


def run(intent: IntentResult, draft: DraftResult) -> ValidationResult:
    issues = []

    if intent.confidence < settings.INTENT_CONFIDENCE_THRESHOLD:
        issues.append(
            f"low intent confidence ({intent.confidence:.2f} < "
            f"{settings.INTENT_CONFIDENCE_THRESHOLD})"
        )

    if not draft.draft_reply or len(draft.draft_reply.strip()) < 10:
        issues.append("draft reply is empty or too short")

    if draft.missing_information:
        issues.append("draft reports missing customer information")

    return ValidationResult(is_valid=len(issues) == 0, issues=issues)
