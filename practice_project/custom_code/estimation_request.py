import frappe

@frappe.whitelist()
def create_estimation_request(opportunity, scope):
    if not scope:
        frappe.throw("Scope is mandatory to create Estimation Request")
        
     # Count how many non-cancelled estimations already exist
    existing_estimations = frappe.get_all(
        "Estimation",
        filters={
            "opportunity": opportunity,
            "docstatus": ["!=", 2]  # ignore Cancelled
        },
        pluck="name"
    )

    if len(existing_estimations) >= 2:
        
        #frappe.throw("Only 2 Estimations are allowed per Opportunity .")
        frappe.throw(
    "Only 2 Estimations are allowed per Opportunity .\n"
    "Existing Estimations: " + ", ".join(existing_estimations)
)



    doc = frappe.new_doc("Estimation")
    doc.opportunity = opportunity
    doc.description = scope
    doc.insert(ignore_permissions=True)
    doc.submit()
    
     # Link the created Estimation back to Opportunity
    #frappe.db.set_value("Opportunity", opportunity, "custom_opportunity", doc.name)
    
    # Clear scope after creation
    frappe.db.set_value("Opportunity", opportunity, "custom_scope", "")


    return doc.name  
