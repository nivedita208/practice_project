# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DailyBusinessDashboard(Document):
	pass

@frappe.whitelist()
def get_dashboard_data(from_date, to_date):
    data = {}

    def get_count(doctype, date_field):
        return frappe.db.count(doctype, {date_field: ["between", [from_date, to_date]]})

    data["sales_orders"] = get_count("Sales Order", "transaction_date")
    data["sales_invoices"] = get_count("Sales Invoice", "posting_date")
    data["quotations"] = get_count("Quotation", "transaction_date")
    data["events"] = get_count("Event", "starts_on")

    return data