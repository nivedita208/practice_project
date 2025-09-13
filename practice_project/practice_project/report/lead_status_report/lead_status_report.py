# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, nowdate

def execute(filters=None):
    columns = [
        {"label": "Lead Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": "0-7 Days", "fieldname": "bucket1", "fieldtype": "Int", "width": 120},
        {"label": "8-14 Days", "fieldname": "bucket2", "fieldtype": "Int", "width": 120},
        {"label": ">15 Days", "fieldname": "bucket3", "fieldtype": "Int", "width": 120},
        {"label": "Total Leads", "fieldname": "total", "fieldtype": "Int", "width": 120},
    ]

    where_clause, values = [], []

    if filters.get("from_date"):
        where_clause.append("l.creation >= %s")
        values.append(filters["from_date"])

    if filters.get("to_date"):
        where_clause.append("l.creation <= %s")
        values.append(filters["to_date"])

    if filters.get("source"):
        where_clause.append("l.source = %s")
        values.append(filters["source"])

    if filters.get("owner"):
        where_clause.append("l.owner = %s")
        values.append(filters["owner"])

    conditions = " AND ".join(where_clause)
    if conditions:
        conditions = "WHERE " + conditions

    leads = frappe.db.sql(f"""
        SELECT name, status, creation
        FROM `tabLead` l
        {conditions}
    """, values, as_dict=True)

    grouped = {}  # empty dictionary that will store the final results
    today = nowdate()  # gets the current system date 

    for l in leads:
        age = date_diff(today, l.creation)
        status = l.status or "Not Specified"

        if status not in grouped:
            grouped[status] = {"bucket1": 0, "bucket2": 0, "bucket3": 0, "total": 0}

        if age <= 7:
            grouped[status]["bucket1"] += 1
        elif 8 <= age <= 14:
            grouped[status]["bucket2"] += 1
        else:
            grouped[status]["bucket3"] += 1

        grouped[status]["total"] += 1

    # build final data list
    data = []
    for status, counts in grouped.items():
        row = {
            "status": status,
            "bucket1": counts["bucket1"],
            "bucket2": counts["bucket2"],
            "bucket3": counts["bucket3"],
            "total": counts["total"],
        }
        data.append(row)

    return columns, data
