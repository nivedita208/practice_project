import frappe
from frappe.utils import nowdate, date_diff

def set_priority_status(doc, method):
    # calculate age of lead in days
    lead_age = date_diff(nowdate(), doc.creation)

    if lead_age >= 14:
        doc.custom_priority_status = "Low Priority"
    else:
        doc.custom_priority_status = "Fresh"
        


def update_old_leads():
    leads = frappe.get_all("Lead", fields=["name", "creation"])
    for l in leads:
        lead_age = frappe.utils.date_diff(frappe.utils.nowdate(), l.creation)
        if lead_age >= 14:
            frappe.db.set_value("Lead", l.name, "custom_priority_status", "Low Priority")
        else:
            frappe.db.set_value("Lead", l.name, "custom_priority_status", "Fresh")

