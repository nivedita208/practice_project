import frappe
from frappe.utils import now_datetime

def create_events_from_meetings(doc, method):
    for meeting in doc.custom_lead_meeting:

        # Check if Event with same summary & date already exists for this Lead
        existing_event = frappe.db.exists("Event", {
            "subject": meeting.summary,
            "starts_on": meeting.meeting_date,
            "lead": doc.name
        })
        if existing_event:
            continue

        # Create Event
        event = frappe.new_doc("Event")
        event.subject = meeting.summary or "Meeting"
        event.description = meeting.description
        event.starts_on = meeting.meeting_date or now_datetime()
        # event.owner = doc.lead_owner
        event.lead = doc.name
        event.save(ignore_permissions=True)

        event.append("event_participants", {
        "reference_doctype": "User",
        "reference_docname": doc.lead_owner
    })

        # Notify Lead owner
        if doc.lead_owner:
            frappe.sendmail(
                recipients=[doc.lead_owner],
                subject=f"New Meeting Scheduled for Lead {doc.name}",
                message=f"""
                    Hello,<br><br>
                    A meeting has been scheduled for your Lead <b>{doc.lead_name}</b>.<br>
                    <b>Summary:</b> {meeting.summary}<br>
                    <b>Date:</b> {meeting.meeting_date}
                """,
                reference_doctype="Lead",
                reference_name=doc.name
            )
        
        
