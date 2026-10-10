
from tools import find_invoice_files, extract_invoice_data

files = find_invoice_files()

print("Invoices found:", len(files))

for file in files:
    result = extract_invoice_data(file)
    print(result)
