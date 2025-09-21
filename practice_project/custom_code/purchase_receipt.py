import frappe
from frappe.utils import nowdate

def purchase_receipt_on_submit(doc, method):
    """
    On Purchase Receipt submission, split each PR line into individual rolls
    and create separate batches with meters.
    """
    for item in doc.items:
        # Only process if custom fields are provided
        if getattr(item, "custom_number_of_rolls", 0) > 0 and getattr(item, "custom_meters_per_roll", 0) > 0:
            num_rolls = int(item.custom_number_of_rolls)
            meters_per_roll = float(item.custom_meters_per_roll)

            for i in range(1, num_rolls + 1):
                # Generate unique batch/roll name
                batch_name = f"{item.item_code}-{nowdate().replace('-', '')}-{i}"  # "MEOW" + "-" + "20250920" + "-" + "1" → "MEOW-20250920-1"

                # Create Batch doc
                batch_doc = frappe.get_doc({
                    "doctype": "Batch",
                    "item": item.item_code,
                    "batch_id": batch_name,          
                    "custom_initial_meters": meters_per_roll,
                    "custom_remaining_meters": meters_per_roll,
                    "custom_roll_number": i                  
                })
                batch_doc.insert(ignore_permissions=True)