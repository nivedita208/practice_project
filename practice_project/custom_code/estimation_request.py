import frappe

@frappe.whitelist()
def create_estimation_request(opportunity, scope):
    if not scope:
        frappe.throw("Scope is mandatory to create Estimation Request")
    
    
    #######################    
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



#-------------------------------------------------------------
#this below  code only 1 draft allowing direclt submitted (max 2 ) not creating when 1 draft is present 
'''import frappe

@frappe.whitelist()
def create_estimation_request(opportunity, scope):
    if not scope:
        frappe.throw("Scope is mandatory to create Estimation Request")

    # Get all non-cancelled Estimations for this Opportunity
    existing_estimations = frappe.get_all(
        "Estimation",
        filters={
            "opportunity": opportunity,
            "docstatus": ["!=", 2]  # ignore Cancelled
        },
        fields=["name", "docstatus"]
    )

    draft_count = 0
    submitted_count = 0
    draft_names = []
    submitted_names = []

    for e in existing_estimations:
        if e.docstatus == 0:
            draft_count += 1
            draft_names.append(e.name)
        elif e.docstatus == 1:
            submitted_count += 1
            submitted_names.append(e.name)

    # Enforce max limits
    if draft_count >= 1 and submitted_count >= 2:
        msg = "Cannot create more Estimations. Limits reached.<br>"
        msg += f"Existing Draft: {', '.join(draft_names)}<br>" if draft_names else ""
        msg += f"Existing Submitted: {', '.join(submitted_names)}"
        frappe.throw(msg)

    # Decide docstatus
    if draft_count == 0:
        # No Draft exists → create Draft
        docstatus_to_create = 0
    else:
        # Draft exists → create Submitted
        if submitted_count >= 2:
            frappe.throw("Cannot create more than 2 Submitted Estimations.")
        docstatus_to_create = 1

    # Create Estimation
    doc = frappe.new_doc("Estimation")
    doc.opportunity = opportunity
    doc.description = scope
    doc.insert(ignore_permissions=True)

    if docstatus_to_create == 1:
        doc.submit()  # make it Submitted

    # Clear scope after creation
    frappe.db.set_value("Opportunity", opportunity, "custom_scope", "")

    return doc.name
'''