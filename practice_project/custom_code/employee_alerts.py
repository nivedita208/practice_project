import frappe
from frappe.utils import today, add_days

def check_employee_validity_alerts():
    """Send alerts before QID/Passport (valid_upto) expiry"""
    employees = frappe.get_all(
        'Employee',
        fields=['name', 'employee_name', 'valid_upto']
    )

    for emp in employees:
        expiry_date = emp.get('valid_upto')
        if expiry_date:
            alert_date = add_days(today(), 30)   # 30 days before expiry
            if expiry_date <= alert_date:
                frappe.sendmail(
                    recipients=['profilezone285@gmail.com'],  # or HR role email
                    subject=f"{emp.employee_name} Valid Upto Expiring Soon",
                    message=f"{emp.employee_name}'s ID/Passport will expire on {expiry_date}."
                )
