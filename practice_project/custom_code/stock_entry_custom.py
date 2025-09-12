import frappe

def validate_stock_entry(doc, method):
    if doc.stock_entry_type == "Material Transfer":
        if doc.from_warehouse == "Printing Area" and doc.to_warehouse == "Main Store":
            frappe.throw("Reverse transfer from Printing Area to Main Store is not allowed.")
