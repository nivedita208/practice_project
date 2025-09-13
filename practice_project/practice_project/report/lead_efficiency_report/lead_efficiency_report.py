# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Lead Source", "fieldname": "source", "fieldtype": "Data", "width": 150},
        {"label": "Lead Owner", "fieldname": "owner", "fieldtype": "Data", "width": 150},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
        {"label": "Total Leads", "fieldname": "total", "fieldtype": "Int", "width": 120},
        {"label": "Converted Leads", "fieldname": "converted", "fieldtype": "Int", "width": 150},
        {"label": "Conversion Ratio (%)", "fieldname": "ratio", "fieldtype": "Percent", "width": 150},
    ]

    where_clause = []
    values = []

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

    data = frappe.db.sql(f"""
        SELECT 
            l.source, 
            l.owner,
            DATE_FORMAT(l.creation, '%%Y-%%m') as month,  -- Year-Month format
            COUNT(*) as total,
            SUM(CASE WHEN l.status='Converted' OR l.customer IS NOT NULL THEN 1 ELSE 0 END) as converted
        FROM `tabLead` l
        {conditions}
        GROUP BY l.source, l.owner, month
        ORDER BY month
    """, values, as_dict=True)

    for d in data:
        d["ratio"] = (d["converted"] / d["total"] * 100) if d["total"] else 0

    return columns, data

