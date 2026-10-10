
def understand_task(task):
    """Classify a user request using local rules."""

    if not task or not task.strip():
        return {
            "supported": False,
            "intent": "empty",
            "scope": None,
            "should_save": False,
            "reason": "No task was provided.",
        }

    task_lower = task.lower()

    invoice_keywords = [
        "invoice",
        "bill",
        "vendor",
        "supplier",
    ]

    if not any(word in task_lower for word in invoice_keywords):
        return {
            "supported": False,
            "intent": "unsupported",
            "scope": None,
            "should_save": False,
            "reason": "Only invoice-related tasks are supported.",
        }

    latest_keywords = [
        "latest",
        "most recent",
        "newest",
    ]

    scope = (
        "latest"
        if any(word in task_lower for word in latest_keywords)
        else "all"
    )

    save_keywords = [
        "save",
        "record",
        "store",
        "process",
        "enter",
    ]

    should_save = any(
        word in task_lower
        for word in save_keywords
    )

    return {
        "supported": True,
        "intent": "invoice_processing",
        "scope": scope,
        "should_save": should_save,
        "reason": "Invoice-related task detected.",
    }


def create_plan(task_info):
    """Create an execution plan from the task classification."""

    if not task_info["supported"]:
        return []

    if task_info["scope"] == "latest":
        plan = [
            "find_latest_invoice",
            "extract_invoice_details",
        ]
    else:
        plan = [
            "find_invoice_files",
            "extract_invoice_details",
        ]

    if task_info["should_save"]:
        plan.extend([
            "save_valid_records",
            "verify_saved_records",
        ])

    return plan
