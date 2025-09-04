import frappe

    
@frappe.whitelist()
def create_estimation_request(opportunity, customer, date=None, product_details=None,
                              qty=None, description=None, category=None,
                              raw_material=None, labor=None, delivery=None,
                              operation=None, total_cost=None, additional_notes=None):
    try:
        # Create new Estimation Doc
        est = frappe.new_doc("Estimation Request")
        est.opportunity = opportunity
        est.customer = customer
        est.estimation_date = date
        est.product_details = product_details
        est.qty = qty
        est.description = description
        est.category = category
        est.raw_material = raw_material
        est.labor = labor
        est.delivery = delivery
        est.operation = operation
        est.total_cost = total_cost
        est.additional_notes = additional_notes

        est.insert(ignore_permissions=True)


        return est.name

    except Exception as e:
        frappe.throw(f"Failed to create Estimation: {str(e)}")
