# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    """
    Roll Meter Balance Report
    Shows all batches with remaining meters and wastage.
    Filters: item, date range, show only remaining meters.
    """

    # Define report columns
    columns = [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Batch / Roll", "fieldname": "batch_id", "fieldtype": "Data", "width": 150},
        {"label": "Roll Number", "fieldname": "custom_roll_number", "fieldtype": "Int", "width": 100},
        {"label": "Initial Meters", "fieldname": "custom_initial_meters", "fieldtype": "Float", "width": 120},
        {"label": "Remaining Meters", "fieldname": "custom_remaining_meters", "fieldtype": "Float", "width": 120},
        {"label": "Wastage", "fieldname": "wastage", "fieldtype": "Float", "width": 100}
    ]

    # Build filter conditions safely using placeholders
    conditions = []
    values = []

    if filters:
        if filters.get("item"):
            conditions.append("item = %s")
            values.append(filters.get("item"))
        if filters.get("from_date"):
            conditions.append("creation >= %s")
            values.append(filters.get("from_date"))
        if filters.get("to_date"):
            conditions.append("creation <= %s")
            values.append(filters.get("to_date"))
        if filters.get("show_only_remaining"):
            conditions.append("custom_remaining_meters > 0")

    # Combine conditions
    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Fetch batches from Batch table
    batches = frappe.db.sql(f"""
        SELECT
            item,
            batch_id,
            custom_roll_number,
            custom_initial_meters,
            custom_remaining_meters,
            (custom_initial_meters - custom_remaining_meters) AS wastage
        FROM `tabBatch`
        {where_clause}
        ORDER BY item, creation ASC
    """, tuple(values), as_dict=1)  # safe placeholder usage

    return columns, batches

