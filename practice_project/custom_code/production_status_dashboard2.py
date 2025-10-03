import frappe
from frappe.utils import today, getdate

# Cost center validation
def validate_cost_center(self, method):
    if self.cost_center:
        existing = frappe.db.exists(
            "Production Status Dashboard2",
            {
                "cost_center": self.cost_center,
                "name": ["!=", self.name]
            }
        )
        if existing:
            frappe.throw(
                f"A Production Status Dashboard already exists for Cost Center '{self.cost_center}'"
            )

@frappe.whitelist()
def get_dashboard_data(cost_center):
    today_date = getdate(today())
    
    # Work Orders
    wos = frappe.get_all(
        "Work Order",
        fields=[
            "name", "status", "planned_end_date", "qty",
            "produced_qty", "production_item", "planned_start_date", "modified"
        ]
    )

    wo_kpis = {
        "pending_wos": 0,
        "in_process_wos": 0,
        "overdue_wos": 0,
        "completed_today_wos": 0
    }

    for wo in wos:
        end_date = wo.planned_end_date
        modified_date = wo.modified.date() if hasattr(wo.modified, "date") else getdate(wo.modified)
        # Completed Today
        if wo.status == "Completed" and modified_date == today_date:
            wo_kpis["completed_today_wos"] += 1
        # Overdue
        elif end_date and getdate(end_date) < today_date and wo.status != "Completed":
            wo_kpis["overdue_wos"] += 1
        # Pending
        elif wo.status == "Not Started":
            wo_kpis["pending_wos"] += 1
        # In Process
        elif wo.status == "In Process":
            wo_kpis["in_process_wos"] += 1

    # Job Cards
    jcs = frappe.get_all(
        "Job Card",
        fields=[
            "name","status","expected_end_date","for_quantity","work_order",
            "operation","workstation","expected_start_date","expected_end_date","modified"
        ]
    )

    jc_kpis = {
        "pending_jcs": 0,
        "in_process_jcs": 0,
        "on_hold_jcs": 0,
        "overdue_jcs": 0,
        "completed_today_jcs": 0
    }

    for jc in jcs:
        end_date = jc.expected_end_date
        modified_date = jc.modified.date() if hasattr(jc.modified, "date") else getdate(jc.modified)
        # Completed Today
        if jc.status == "Completed" and modified_date == today_date:
            jc_kpis["completed_today_jcs"] += 1
        # Overdue
        elif end_date and getdate(end_date) < today_date and jc.status != "Completed":
            jc_kpis["overdue_jcs"] += 1
        # Pending
        elif jc.status == "Open":
            jc_kpis["pending_jcs"] += 1
        # In Process
        elif jc.status == "Work in Progress":
            jc_kpis["in_process_jcs"] += 1
        # On Hold
        elif jc.status == "On Hold":
            jc_kpis["on_hold_jcs"] += 1

    return {
        "kpis": {**wo_kpis, **jc_kpis},
        "work_orders": wos,
        "job_cards": jcs
    }
