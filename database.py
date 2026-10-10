
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "invoices.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                company TEXT NOT NULL,
                amount REAL NOT NULL,
                due_date TEXT NOT NULL,
                UNIQUE(company, file_name)
            )
        """)


def save_invoice(invoice):
    required = ["file", "company", "amount", "due_date"]

    if any(not invoice.get(key) for key in required):
        return {
            "success": False,
            "message": "Invoice is missing required fields."
        }

    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO invoices
                    (file_name, company, amount, due_date)
                VALUES (?, ?, ?, ?)
            """, (
                invoice["file"],
                invoice["company"],
                float(invoice["amount"]),
                invoice["due_date"]
            ))

        return {"success": True, "message": "Invoice saved."}

    except sqlite3.IntegrityError:
        return {
            "success": False,
            "message": "Duplicate invoice record."
        }


def get_all_invoices():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, file_name, company, amount, due_date
            FROM invoices
            ORDER BY id DESC
        """).fetchall()

    return [
        {
            "id": row[0],
            "file": row[1],
            "company": row[2],
            "amount": row[3],
            "due_date": row[4]
        }
        for row in rows
    ]
