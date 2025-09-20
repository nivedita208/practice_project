# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate

def execute(filters=None):
    # Columns
    columns = [
        {"label": "Work Order", "fieldname": "work_order", "fieldtype": "Link", "options": "Work Order", "width": 350},
        {"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Planned Qty", "fieldname": "planned_qty", "fieldtype": "Float", "width": 120},
        {"label": "Consumed Qty", "fieldname": "consumed_qty", "fieldtype": "Float", "width": 120},
        {"label": "Wastage Qty", "fieldname": "wastage_qty", "fieldtype": "Float", "width": 120},
        {"label": "Wastage %", "fieldname": "wastage_percent", "fieldtype": "Percent", "width": 100},
    ]

    data = []
    filters = filters or {}
    conditions = []
    values = []

    # Add filters
    if filters.get("work_order"):
        conditions.append("wl.parent = %s")
        values.append(filters.get("work_order"))
    if filters.get("item_code"):
        conditions.append("wl.item_code = %s")
        values.append(filters.get("item_code"))
    if filters.get("from_date"):
        conditions.append("wl.date >= %s")
        values.append(filters.get("from_date"))
    if filters.get("to_date"):
        conditions.append("wl.date <= %s")
        values.append(filters.get("to_date"))

    condition_sql = " AND ".join(conditions)
    if condition_sql:
        condition_sql = "WHERE " + condition_sql

    # Fetch wastage entries using placeholders
    wastage_entries = frappe.db.sql(f"""
        SELECT
            wl.parent AS work_order,
            wl.item_code,
            wl.planned_qty,
            wl.consumed_qty,
            wl.wastage_qty
        FROM `tabWO Wastage Log` wl
        {condition_sql}
    """, values=values, as_dict=True)

    # Calculate wastage %
    for d in wastage_entries:
        d["wastage_percent"] = (d["wastage_qty"] / d["planned_qty"] * 100) if d["planned_qty"] else 0
        data.append(d)

    return columns, data




