# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MockupOrder(Document):
	pass


# def update_so_design_status(doc, method):
#     # Ensure MO is linked to a Sales Order
#     if doc.sales_order:
#         try:
#             # Check if any item in the child table is approved
#             approved = False
#             for row in doc.items:  #items is childtable fieldname
#                 if row.approval_status == "Approved":
#                     approved = True
#                     break

#             # If any item is approved, update SO
#             if approved:
#                 frappe.db.set_value("Sales Order", doc.sales_order, "design_status", "Approved")
#                 frappe.msgprint(f"SO {doc.sales_order} design_status updated to Approved")

#         except Exception as e:
#             frappe.log_error(f"Error updating SO design_status: {e}", "Mockup Order -> SO update")