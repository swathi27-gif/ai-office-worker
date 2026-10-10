
from tools import find_invoice_files, extract_invoice_data
from database import initialize_database, save_invoice, get_all_invoices

initialize_database()

files = find_invoice_files()

if not files:
    print("No invoices found.")
else:
    invoice = extract_invoice_data(files[0])
    result = save_invoice(invoice)
    print("Save result:", result)

    print("\nSaved invoice records:")
    for record in get_all_invoices():
        print(record)
