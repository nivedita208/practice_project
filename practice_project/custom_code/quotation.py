import frappe

def validate_quotation(doc, method):
    # Get Customer Type from Customer master
    if doc.customer:
        customer_type = frappe.get_value("Customer", doc.customer, "customer_type")

        if customer_type == "Individual":
            if not doc.customer_name:
                frappe.throw("Customer Name is mandatory for Individual customers")
            if not doc.custom_mobile_number:
                frappe.throw("Mobile Number is mandatory for Individual customers")
