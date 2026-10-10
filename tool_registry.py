
from tools import find_invoice_files, extract_invoice_data
from database import initialize_database, save_invoice, get_all_invoices


def find_all_invoices():
    """Return all invoice PDF paths."""
    return find_invoice_files()


def find_latest_invoice():
    """Return the most recently modified invoice PDF."""
    files = find_invoice_files()

    if not files:
        return []

    latest = max(files, key=lambda file: file.stat().st_mtime)
    return [latest]


def extract_details(file):
    """Extract invoice details from one PDF."""
    return extract_invoice_data(file)


def save_valid_invoice(invoice):
    """Save an invoice only if its required fields are present."""
    required = ["company", "amount", "due_date"]

    missing = [
        field for field in required
        if invoice.get(field) is None
        or str(invoice.get(field)).strip() == ""
    ]

    if missing:
        return {
            "success": False,
            "message": "Missing fields: " + ", ".join(missing),
        }

    initialize_database()
    return save_invoice(invoice)


def verify_invoice(invoice):
    """Verify an invoice against the stored database record."""
    records = get_all_invoices()

    for record in records:
        try:
            matches = (
                record["file"] == invoice["file"]
                and record["company"] == invoice["company"]
                and float(record["amount"]) == float(invoice["amount"])
                and record["due_date"] == invoice["due_date"]
            )
        except (KeyError, TypeError, ValueError):
            matches = False

        if matches:
            return {
                "success": True,
                "message": "Stored invoice verified.",
            }

    return {
        "success": False,
        "message": "No matching stored invoice found.",
    }


# Each planned action maps to a real Python function.
TOOL_REGISTRY = {
    "find_invoice_files": find_all_invoices,
    "find_latest_invoice": find_latest_invoice,
    "extract_invoice_details": extract_details,
    "save_valid_records": save_valid_invoice,
    "verify_saved_records": verify_invoice,
}


def execute_tool(name, **kwargs):
    """Execute a registered tool and return a consistent result."""
    tool = TOOL_REGISTRY.get(name)

    if tool is None:
        return {
            "success": False,
            "data": None,
            "error": f"Unknown tool: {name}",
        }

    try:
        data = tool(**kwargs)

        return {
            "success": True,
            "data": data,
            "error": None,
        }

    except Exception as exc:
        return {
            "success": False,
            "data": None,
            "error": f"{type(exc).__name__}: {exc}",
        }
