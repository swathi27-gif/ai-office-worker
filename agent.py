
from planner import understand_task, create_plan
from tool_registry import execute_tool


def run_agent(task):
    """Plan, execute registered tools, and verify invoice outcomes."""

    logs = []
    results = []

    def log(message):
        logs.append(message)

    # Step 1: Understand the request.
    task_info = understand_task(task)

    if not task_info["supported"]:
        status = (
            "failed"
            if task_info["intent"] == "empty"
            else "unsupported"
        )
        return {
            "status": status,
            "logs": [task_info["reason"]],
            "results": [],
        }

    log("UNDERSTAND: " + task_info["reason"])

    # Step 2: Create the plan.
    plan = create_plan(task_info)
    log("PLAN: " + " -> ".join(plan))

    # Step 3: Execute the search tool selected by the planner.
    search_tool = plan[0]
    log(f"EXECUTE: Running tool '{search_tool}'.")

    search_result = execute_tool(search_tool)

    if not search_result["success"]:
        log("FAILED: " + search_result["error"])
        return {
            "status": "failed",
            "logs": logs,
            "results": [],
        }

    files = search_result["data"]

    if not files:
        log("OBSERVE: No PDF invoices found.")
        return {
            "status": "failed",
            "logs": logs,
            "results": [],
        }

    log(f"OBSERVE: Found {len(files)} PDF invoice(s).")

    all_verified = True
    valid_count = 0

    # Step 4: Extract invoice details using the registry.
    for file in files:
        log(f"EXECUTE: Reading {file.name}.")

        extraction = None

        for attempt in range(1, 3):
            extraction = execute_tool(
                "extract_invoice_details",
                file=file,
            )

            if extraction["success"]:
                break

            log(
                f"OBSERVE: Extraction attempt {attempt} failed for "
                f"{file.name}: {extraction['error']}"
            )

        if not extraction or not extraction["success"]:
            all_verified = False
            log(f"FAILED: Could not read {file.name}.")
            continue

        invoice = extraction["data"]

        result = {
            "file": invoice["file"],
            "company": invoice["company"],
            "amount": invoice["amount"],
            "due_date": invoice["due_date"],
        }
        results.append(result)

        log(f"OBSERVE: Extracted details from {file.name}.")

        # Reject incomplete data before any database write.
        required = ["company", "amount", "due_date"]

        missing = [
            field for field in required
            if invoice.get(field) is None
            or str(invoice.get(field)).strip() == ""
        ]

        if missing:
            all_verified = False
            log(
                f"NEEDS REVIEW: {file.name} is missing "
                f"{', '.join(missing)}. Record not saved."
            )
            continue

        valid_count += 1

        if not task_info["should_save"]:
            log(f"EXTRACTED: {file.name}; no save requested.")
            continue

        # Step 5: Save through the approved registry tool.
        save_result = execute_tool(
            "save_valid_records",
            invoice=invoice,
        )

        if not save_result["success"]:
            all_verified = False
            log(f"FAILED: Save operation for {file.name}: "
                f"{save_result['error']}")
            continue

        if not save_result["data"]["success"]:
            all_verified = False
            log(
                f"NEEDS REVIEW: {save_result['data']['message']}"
            )
            continue

        # Step 6: Verify through the approved registry tool.
        verification = execute_tool(
            "verify_saved_records",
            invoice=invoice,
        )

        if verification["success"] and verification["data"]["success"]:
            log(
                f"VERIFIED: {file.name} matches the database record."
            )
        else:
            all_verified = False

            if verification["success"]:
                error = verification["data"]["message"]
            else:
                error = verification["error"]

            log(f"VERIFICATION FAILED: {file.name}: {error}")

    # Step 7: Return an honest final status.
    if not all_verified:
        status = "needs_review"
    elif task_info["should_save"]:
        status = "completed"
    else:
        status = "extracted"

    if status == "completed":
        log(
            f"COMPLETE: {valid_count} valid invoice(s) "
            "processed and verified."
        )
    elif status == "extracted":
        log("COMPLETE: Invoice information extracted without saving.")
    else:
        log("INCOMPLETE: Some invoices need review or failed.")

    return {
        "status": status,
        "logs": logs,
        "results": results,
    }
