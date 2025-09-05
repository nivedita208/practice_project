import frappe

def validate_sales_invoice(doc, method):
    if not doc.custom_quotation:
        frappe.throw("Quotation is mandatory before creating a Sales Invoice.")
