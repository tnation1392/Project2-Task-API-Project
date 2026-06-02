from fastapi import HTTPException

ALLOWED_TASK_TRANSITIONS = {
    "todo": ["in_progress"],
    "in_progress": ["done"],
    "done": [],
}


def validate_task_transition(current_status: str, new_status: str) -> None:
    allowed_next_statuses = ALLOWED_TASK_TRANSITIONS.get(current_status, [])

    if new_status not in allowed_next_statuses:
        raise HTTPException(
            status_code=409,
            detail=f"Invalid status transition from '{current_status}' to '{new_status}'",
        )
