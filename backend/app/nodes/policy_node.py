from app.core.schemas import Intent, PolicyResult
from app.data.policies import get_policy


def run(intent: Intent) -> PolicyResult:
    policy = get_policy(intent.value)
    if policy is None:
        return PolicyResult(
            found=False,
            content="No specific policy found for this intent. Respond using general guidance.",
        )
    return PolicyResult(
        policy_id=policy["policy_id"],
        title=policy["title"],
        content=policy["content"],
        found=True,
    )
