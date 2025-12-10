# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document
class VehicleList(Document):

    def before_insert(self):
        if not self.status:
            self.status = "Draft"

'''
q1. Defaults: You add a field status (Select: Draft, Submitted) to a DocType. It must default to "Draft" on new document creation.

Describe one correct way to ensure this in Frappe (server hook, client script, or DocType default). Include a 3–6 line snippet or precise steps.
q2. Validation: Prevent saving a Purchase Order if supplier_approval_state ≠ "Approved".

Where would you implement this and what would the minimal code / logic look like?
q3. Debugging: A user says "My Purchase Order isn't saving." Outline your first 4 steps to isolate the issue in Frappe (logs, console, validation, workflow, permissions).
*
q4. Reporting: You need a report of Purchase Order count by supplier for the last 30 days.
Write an SQL (or Frappe ORM) example that reasonably produces this.
q5. Learning Plan: In your first 4 weeks, how would you ramp up on Frappe to ship your first feature safely?
List 4–6 bullet points (you can write them as lines).

'''     
     


