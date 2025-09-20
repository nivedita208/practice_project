import frappe

def validate_work_order(doc, method):
    if doc.sales_order and doc.sales_order_item:
        so_item_status = frappe.db.get_value("Sales Order Item", doc.sales_order_item, "custom_design_status")
        if so_item_status != "Approved":
            frappe.throw("Cannot create Work Order: Design Mockup is not approved for this Sales Order line.")

            
def create_job_cards(doc, method):
    bom_operations = frappe.get_all("BOM Operation",  #childtable name
        filters={"parent": doc.bom_no},
        fields=["operation", "time_in_mins", "workstation"]
    )
    for op in bom_operations:
        jc = frappe.new_doc("Job Card")
        jc.work_order = doc.name
        jc.operation = op.operation
        jc.for_quantity = doc.qty
        jc.workstation = op.workstation
        jc.insert(ignore_permissions=True)
        

@frappe.whitelist()
def make_stock_adjustment(work_order, purpose):
    wo = frappe.get_doc("Work Order", work_order)

    se = frappe.new_doc("Stock Entry")
    se.company = wo.company
    se.work_order = wo.name

    # set correct type
    if purpose == "Material Issue":
        se.stock_entry_type = "Material Issue"
    else:
        se.stock_entry_type = "Material Receipt"

    # optional: prefill child table with WO items
    for item in wo.required_items:
        se.append("items", {
            "item_code": item.item_code,
            "qty": 0,  # user will update adjustment qty
            "s_warehouse": item.source_warehouse if purpose == "Material Issue" else "",
            "t_warehouse": wo.fg_warehouse if purpose == "Material Receipt" else ""
        })

    return se.as_dict()



