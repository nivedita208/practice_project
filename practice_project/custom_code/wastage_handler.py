import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def update_wastage_on_stock_entry(doc, method):
    """
    This function runs when a Stock Entry is submitted.
    It logs wastage in the Work Order linked to this Stock Entry.
    """

    # Check if this Stock Entry is linked to a Work Order
    if doc.work_order:
        wo = frappe.get_doc("Work Order", doc.work_order)

        # Loop through each item row in the Stock Entry
        for item in doc.items:
            # Only process rows where wastage_qty > 0
            if item.wastage_qty > 0:
                # Add a new row in Work Order's wastage log
                wo.append("wastage_log", {
                    "item_code": item.item_code,
                    "planned_qty": item.qty,
                    "consumed_qty": item.transfer_qty,
                    "wastage_qty": item.wastage_qty,
                    "date": nowdate()
                })

        # Save the Work Order to store the wastage log
        wo.save(ignore_permissions=True)
