import frappe

def stock_entry_validate(doc, method):
    """
    Validate and allocate meters from batches when issuing stock.
    Auto-pick batches in FIFO order and deduct meters.
    """
    for item in doc.items:
        # Only process items with meters per roll
        if getattr(item, "custom_meters_per_roll", 0) > 0:
            required_meters = float(item.custom_meters_per_roll)
            item_code = item.item_code

            allocated = 0  # total meters allocated so far

            # Fetch available batches with remaining meters > 0, oldest first
            batches = frappe.get_all(
                "Batch",
                filters={"item": item_code, "custom_remaining_meters": [">", 0]},
                fields=["name", "custom_remaining_meters"],
                order_by="creation asc"
            )

            for batch in batches:
                if allocated >= required_meters:
                    break

                available = batch.custom_remaining_meters
                deduct = min(available, required_meters - allocated)

                # Deduct meters from batch
                frappe.db.set_value(
                    "Batch",
                    batch.name,
                    "custom_remaining_meters",
                    available - deduct
                )

                allocated += deduct

            # If not enough meters were available
            if allocated < required_meters:
                frappe.throw(
                    f"Not enough meters available for item {item_code}. "
                    f"Requested: {required_meters}, available: {allocated}"
                )





def validate_stock_entry(doc, method):
    if doc.stock_entry_type == "Material Transfer":
        if doc.from_warehouse == "Printing Area" and doc.to_warehouse == "Main Store":
            frappe.throw("Reverse transfer from Printing Area to Main Store is not allowed.")

