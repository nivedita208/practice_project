import frappe

def check_quotation_approval(doc, method):
    # Ensure Sales Order has a Quotation linked
    if doc.quotation:
        quotation_status = frappe.db.get_value("Quotation", doc.quotation, "workflow_state")
        if quotation_status != "Approved":
            frappe.throw("You can only create a Sales Order from an Approved Quotation.")
