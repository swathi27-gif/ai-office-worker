
from agent import run_agent


def test_empty_task():
    result = run_agent("")

    assert result["status"] == "failed"
    print("PASS: Empty task is rejected.")


def test_unsupported_task():
    result = run_agent("Summarize today's weather.")

    assert result["status"] == "unsupported"
    print("PASS: Unsupported task is rejected.")


def test_latest_invoice_selection():
    result = run_agent(
        "Find the latest invoice and save its amount and due date."
    )

    assert len(result["results"]) == 1, (
        "Latest-invoice task should process exactly one PDF."
    )

    assert result["results"][0]["file"] == "incomplete_invoice.pdf", (
        "Expected the latest modified invoice to be selected."
    )

    assert result["status"] == "needs_review", (
        "Incomplete invoice should require review."
    )

    assert any(
        "Record not saved" in message
        for message in result["logs"]
    ), "Agent did not report that the incomplete record was not saved."

    print("PASS: Latest invoice selected and incomplete data rejected.")


def test_extraction_only():
    result = run_agent("Extract invoice details.")

    assert result["status"] in ("extracted", "needs_review")
    assert any(
        item["company"] == "ABC Technologies"
        and item["amount"] == "12500.00"
        and item["due_date"] == "31/10/2026"
        for item in result["results"]
    ), "Valid invoice details were not extracted."

    print("PASS: Extraction works without requesting a save.")


if __name__ == "__main__":
    test_empty_task()
    test_unsupported_task()
    test_latest_invoice_selection()
    test_extraction_only()

    print("\nAll tests passed!")
