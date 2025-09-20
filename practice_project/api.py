import frappe

def create_mockup_for_so(doc, method):
    if doc.doctype != "Sales Order":
        return

    mockup = frappe.new_doc("Mockup Order")
    mockup.sales_order = doc.name

    # Loop through Sales Order Items and add into Mockup Items
    for so_item in doc.items:
        mockup.append("items", {  # replace with your child table fieldname
            "sales_order_item": so_item.name,
            "sample_quantity": so_item.qty,
            "approval_status": "Pending"  # default
        })

    mockup.insert(ignore_permissions=True)
    frappe.msgprint(f" Mockup Order <b>{mockup.name}</b> created for Sales Order {doc.name}")
    
    
# def sync_mockup_to_so(doc, method):
#     """Sync Mockup Item approval + attachment to linked Sales Order Item"""
#     if not doc.sales_order_item:
#         return

#     # Update design status in Sales Order Item
#     frappe.db.set_value("Sales Order Item", doc.sales_order_item, "design_status", doc.approval_status)

#     # If attachment exists → link it to Sales Order Item too
#     if doc.attachment:
#         _attach_file_to_so_item(doc)

# def _attach_file_to_so_item(mockup_item):
#     """Helper: copy attachment from Mockup Item to Sales Order Item"""
#     file = frappe.get_doc("File", {"file_url": mockup_item.attachment})
#     if file:
#         # Link file to Sales Order Item
#         file_attached = frappe.new_doc("File")
#         file_attached.file_url = file.file_url
#         file_attached.attached_to_doctype = "Sales Order Item"
#         file_attached.attached_to_name = mockup_item.sales_order_item
#         file_attached.insert(ignore_permissions=True)



@frappe.whitelist()
def approve_all_mockup_items(mockup_name):
    """Approve all items if attachments are present"""
    mockup = frappe.get_doc("Mockup Order", mockup_name)
    for item in mockup.items:
        if not item.attachment:
            frappe.throw(f"Attachment missing for item {item.sales_order_item}")
        item.approval_status = "Approved"
    mockup.save()
    return "All items approved"

