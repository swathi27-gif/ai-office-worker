
from unittest.mock import patch

from tools import extract_invoice_data, find_invoice_files
from agent import run_agent


def test_invoice_files_exist():
    files = find_invoice_files()
    assert len(files) >= 1, "No PDF invoices found."
    print("PASS: Invoice PDFs can be discovered.")


def test_valid_invoice_extraction():
    files = find_invoice_files()
    valid_file = next(
        (file for file in files if file.name == "sample_invoice.pdf"),
        None,
    )

    assert valid_file is not None, "Sample invoice PDF is missing."

    invoice = extract_invoice_data(valid_file)

    assert invoice["company"] == "ABC Technologies"
    assert invoice["amount"] == "12500.00"
    assert invoice["due_date"] == "31/10/2026"

    print("PASS: Valid invoice fields are extracted correctly.")


def test_incomplete_invoice_detection():
    files = find_invoice_files()
    incomplete_file = next(
        (file for file in files if file.name == "incomplete_invoice.pdf"),
        None,
    )

    assert incomplete_file is not None, "Incomplete invoice PDF is missing."

    invoice = extract_invoice_data(incomplete_file)

    assert invoice["company"] == "Demo Technologies"
    assert invoice["amount"] is None
    assert invoice["due_date"] is None

    print("PASS: Missing invoice fields are detected.")


def test_unreadable_invoice_retry():
    with patch(
        "tool_registry.extract_invoice_data",
        side_effect=ValueError("Simulated PDF read failure"),
    ):
        result = run_agent("Extract invoice details.")

    assert result["status"] == "needs_review", result
    assert any(
        "Extraction attempt 1 failed" in message
        for message in result["logs"]
    ), result["logs"]
    assert any(
        "Extraction attempt 2 failed" in message
        for message in result["logs"]
    ), result["logs"]
    assert any(
        "Could not read" in message
        for message in result["logs"]
    ), result["logs"]

    print("PASS: Failed extraction is retried twice and reported.")


def test_database_failure():
    files = find_invoice_files()
    valid_file = next(
        (file for file in files if file.name == "sample_invoice.pdf"),
        None,
    )

    assert valid_file is not None, "Sample invoice PDF is missing."

    # Patch the functions where tool_registry looks them up.
    with patch(
        "tool_registry.find_invoice_files",
        return_value=[valid_file],
    ), patch(
        "tool_registry.find_latest_invoice",
        return_value=[valid_file],
    ), patch(
        "tool_registry.save_invoice",
        side_effect=RuntimeError("Simulated database failure"),
    ) as mock_save:
        result = run_agent(
            "Find the latest invoice and save its amount and due date."
        )

    assert mock_save.called, (
        "Save was not attempted. Execution logs: "
        + repr(result["logs"])
    )

    assert result["status"] == "needs_review", result

    assert any(
        "Save operation" in message
        for message in result["logs"]
    ), result["logs"]

    assert any(
        "Simulated database failure" in message
        for message in result["logs"]
    ), result["logs"]

    print("PASS: Database failure is handled without crashing.")


if __name__ == "__main__":
    test_invoice_files_exist()
    test_valid_invoice_extraction()
    test_incomplete_invoice_detection()
    test_unreadable_invoice_retry()
    test_database_failure()

    print("\nAll reliability tests passed!")
