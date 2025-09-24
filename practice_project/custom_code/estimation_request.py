import frappe

@frappe.whitelist()
def create_estimation_request(opportunity, scope):
    if not scope:
        frappe.throw("Scope is mandatory to create Estimation Request")

    doc = frappe.new_doc("Estimation")
    doc.opportunity = opportunity
    doc.description = scope
    doc.insert(ignore_permissions=True)
    
     # Link the created Estimation back to Opportunity
    frappe.db.set_value("Opportunity", opportunity, "custom_opportunity", doc.name)

    return doc.name  
