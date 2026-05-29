from app.core.schemas import AgentTrace, FinalResponse, RouterAction
from app.nodes import (
    draft_node,
    intent_node,
    policy_node,
    priority_node,
    router_node,
    validation_node,
)


def run_agent(message: str) -> FinalResponse:
    trace = AgentTrace()

    trace.intent = intent_node.run(message)
    trace.priority = priority_node.run(message, trace.intent.intent)
    trace.policy = policy_node.run(trace.intent.intent)
    trace.draft = draft_node.run(message, trace.intent, trace.priority, trace.policy)
    trace.validation = validation_node.run(trace.intent, trace.draft)
    trace.router = router_node.run(trace.priority, trace.validation)

    if trace.router.action == RouterAction.SEND_REPLY:
        final_reply = trace.draft.draft_reply
    elif trace.router.action == RouterAction.ASK_FOR_MORE_INFO:
        needed = ", ".join(trace.draft.missing_information) or "more details"
        final_reply = f"Could you please provide {needed} so we can assist you?"
    else:
        final_reply = "Your request has been escalated to a specialist who will contact you shortly."

    return FinalResponse(
        message=message,
        final_reply=final_reply,
        action=trace.router.action,
        trace=trace,
    )
