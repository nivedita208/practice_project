// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Undeposited Cheques"] = {
    "filters": [
        {
            "fieldname": "mode_of_payment",
            "label": "Mode of Payment",
            "fieldtype": "Link",
            "options": "Mode of Payment"
        },
        {
            "fieldname": "payment_type",
            "label": "Payment Type",
            "fieldtype": "Select",
            "options": "\nReceive\nPay\nInternal Transfer"
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": "\nDraft\nSubmitted\nCancelled"
        },
        {
            "fieldname": "custom_reference_status",
            "label": "Reference Status",
            "fieldtype": "Select",
            "options": "\nCollected\nDeposited"
        },
        {
            "fieldname": "posting_date",
            "label": "Posting Date",
            "fieldtype": "Date"
        }
    ]
};

