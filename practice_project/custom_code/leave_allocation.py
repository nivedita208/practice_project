import frappe
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta

def auto_leave_allocation(doc, method):
    """
    Auto-allocate leave based on leave type and service years
    
    """
    employee = frappe.get_doc("Employee", doc.employee)
    doj = employee.date_of_joining
    years_of_service = relativedelta(getdate(), doj).years

    if doc.leave_type == "Annual":
        doc.total_leaves_allocated = 21 if years_of_service < 5 else 30
    elif doc.leave_type == "Casual":
        doc.total_leaves_allocated = 7
    elif doc.leave_type == "Sick":
        doc.total_leaves_allocated = 14
        doc.additional_half_days = 28  # beyond no-pay
    elif doc.leave_type == "Emergency":
        doc.total_leaves_allocated = 7
    elif doc.leave_type == "Bereavement":
        doc.total_leaves_allocated = 15
