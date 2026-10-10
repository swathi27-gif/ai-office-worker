import re
from pathlib import Path
import pymupdf

INVOICE_DIR = Path(__file__).parent / "invoices"


def find_invoice_files():
    """Find all PDF invoices in the invoices folder."""
    return sorted(INVOICE_DIR.glob("*.pdf"))


def extract_invoice_data(pdf_path):
    """Extract basic invoice details from a PDF."""
    pdf_path = Path(pdf_path)

    with pymupdf.open(pdf_path) as document:
        text = "\n".join(page.get_text() for page in document)

    amount_match = re.search(
        r"(?:total amount|grand total|amount due|total)\s*[:\-]?\s*"
        r"(?:INR|Rs\.?|₹|\$)?\s*([\d,]+(?:\.\d{1,2})?)",
        text,
        re.IGNORECASE,
    )

    due_date_match = re.search(
        r"(?:due date|payment due)\s*[:\-]?\s*"
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        text,
        re.IGNORECASE,
    )

    company_match = re.search(
        r"(?:company|vendor|supplier)\s*[:\-]\s*(.+)",
        text,
        re.IGNORECASE,
    )

    return {
        "file": pdf_path.name,
        "company": company_match.group(1).strip() if company_match else None,
        "amount": amount_match.group(1).replace(",", "") if amount_match else None,
        "due_date": due_date_match.group(1) if due_date_match else None,
        "extracted_text": text,
    }
