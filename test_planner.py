
from planner import understand_task, create_plan


def test_latest_invoice_task():
    info = understand_task(
        "Find the latest invoice and save its amount and due date."
    )

    assert info["supported"] is True
    assert info["scope"] == "latest"
    assert info["should_save"] is True

    plan = create_plan(info)

    assert plan == [
        "find_latest_invoice",
        "extract_invoice_details",
        "save_valid_records",
        "verify_saved_records",
    ]

    print("PASS: Latest-invoice task produces the correct plan.")


def test_extraction_only_task():
    info = understand_task("Extract invoice details.")

    assert info["supported"] is True
    assert info["should_save"] is False

    plan = create_plan(info)

    assert "save_valid_records" not in plan
    assert "verify_saved_records" not in plan

    print("PASS: Extraction-only task does not plan database writes.")


def test_all_invoices_task():
    info = understand_task(
        "Find invoices and save their amounts and due dates."
    )

    assert info["scope"] == "all"
    assert info["should_save"] is True

    plan = create_plan(info)

    assert plan[0] == "find_invoice_files"
    assert "save_valid_records" in plan

    print("PASS: All-invoices task produces the correct plan.")


def test_unsupported_task():
    info = understand_task("Summarize today's weather.")

    assert info["supported"] is False
    assert create_plan(info) == []

    print("PASS: Unsupported task is rejected by the planner.")


def test_empty_task():
    info = understand_task("")

    assert info["supported"] is False
    assert info["intent"] == "empty"

    print("PASS: Empty task is rejected by the planner.")


if __name__ == "__main__":
    test_latest_invoice_task()
    test_extraction_only_task()
    test_all_invoices_task()
    test_unsupported_task()
    test_empty_task()

    print("\nAll planner tests passed!")
