import frappe

def block_payroll_if_ssa_not_approved(doc, method):
    """
    Block Payroll Entry creation unless SSA workflow is approved
    """
    ssa_status = frappe.get_value(
        "Salary Structure Assignment",
        {"employee": doc.employee},
        "workflow_state"
    )
    if ssa_status != "Approved":
        frappe.throw("Payroll Entry cannot be created without SSA approval.")
