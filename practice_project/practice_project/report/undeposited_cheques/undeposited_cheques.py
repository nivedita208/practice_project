# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # --------- Columns ---------
    columns = [
        {"label": "Payment Entry", "fieldname": "name", "fieldtype": "Link", "options": "Payment Entry", "width": 150},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Party Type", "fieldname": "party_type", "fieldtype": "Link", "options": "DocType", "width": 120},
        {"label": "Party", "fieldname": "party", "fieldtype": "Dynamic Link", "options": "party_type", "width": 150},
        {"label": "Mode of Payment", "fieldname": "mode_of_payment", "fieldtype": "Link", "options": "Mode of Payment", "width": 120},
        {"label": "Cheque No", "fieldname": "reference_no", "fieldtype": "Data", "width": 120},
        {"label": "Cheque Date", "fieldname": "reference_date", "fieldtype": "Date", "width": 100},
        {"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Select", "options": "Draft\nSubmitted\nCancelled", "width": 100},
        {"label": "Reference Status", "fieldname": "custom_reference_status", "fieldtype": "Select", "options": "Collected\nDeposited", "width": 120},
        {"label": "Invoice Number" , "fieldname": "invoice_number", "fieldtype": "Dynamic Link","options":"reference_doctype", "width": 150},
    ]

    # --------- Conditions ---------
    conditions = []
    values = {}

    if filters.get("mode_of_payment"):
        conditions.append("pe.mode_of_payment = %(mode_of_payment)s")
        values["mode_of_payment"] = filters["mode_of_payment"]

    if filters.get("status"):
        conditions.append("pe.status = %(status)s")
        values["status"] = filters["status"]

    if filters.get("custom_reference_status"):
        conditions.append("pe.custom_reference_status = %(custom_reference_status)s")
        values["custom_reference_status"] = filters["custom_reference_status"]
    else:
        # Default: only show Collected
        conditions.append("pe.custom_reference_status = 'Collected'")


    if filters.get("payment_type"):
        conditions.append("pe.payment_type = %(payment_type)s")
        values["payment_type"] = filters["payment_type"]

    if filters.get("posting_date"):
        conditions.append("pe.posting_date = %(posting_date)s")
        values["posting_date"] = filters["posting_date"]

    # Always ensure only undeposited cheques are shown
    conditions.append("(pe.clearance_date IS NULL OR pe.clearance_date = '')")

    where_clause = " AND ".join(conditions)

    # --------- Query ---------
    data = frappe.db.sql(f"""
        SELECT 
            pe.name,
            pe.posting_date,
            pe.party_type,
            pe.party,
            pe.mode_of_payment,
            pe.reference_no,
            pe.reference_date,
            pe.paid_amount,
            pe.status,
            pe.custom_reference_status,
            per.reference_doctype,
            per.reference_name as invoice_number
        FROM `tabPayment Entry` pe
        LEFT JOIN `tabPayment Entry Reference` per
            ON pe.name = per.parent
        WHERE {where_clause}
        ORDER BY pe.posting_date DESC
    """, values, as_dict=1)

    return columns, data


