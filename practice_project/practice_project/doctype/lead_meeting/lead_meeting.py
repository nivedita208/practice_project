# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class LeadMeeting(Document):
	pass

def create_event_on_meeting_insert(doc, method):
    """
    Triggered when a new row is added in the  Lead Meeting child table.
    Creates an Event linked to the parent Lead.
    """
    # Avoid creating duplicate events
    if getattr(doc, "custom_event_created", 0):
        return

    # Get parent Lead
    parent = frappe.get_doc("Lead", doc.parent)

    # Create Event
    event = frappe.new_doc("Event")
    event.subject = doc.summary or "Meeting"
    event.description = doc.description
    event.starts_on = doc.meeting_date or now_datetime()
    event.reference_doctype = "Lead"
    event.reference_docname = doc.parent

    # Participants
    if parent.lead_owner:
        event.append("event_participants", {
            "reference_doctype": "User",
            "reference_docname": parent.lead_owner
        })

    event.append("event_participants", {
        "reference_doctype": "Lead",
        "reference_docname": doc.parent
    })

    # Reminder
    if getattr(doc, "reminder", 0):
        event.send_reminder = 1

    # Save Event
    event.save(ignore_permissions=True)

    # Mark row as Event created
    doc.custom_event_created = 1
    frappe.db.set_value(doc.doctype, doc.name, "custom_event_created", 1)
