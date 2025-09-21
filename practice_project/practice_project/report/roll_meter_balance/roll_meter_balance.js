// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Roll Meter Balance"] = {
	"filters": [
		{
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "show_only_remaining",
            "label": __("Show Only Remaining"),
            "fieldtype": "Check",
            "default": 1
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        // Highlight wastage in red if > 0
        if (column.fieldname === "wastage" && value > 0) {
            value = `<span style="color:red;font-weight:bold;">${value}</span>`;
        }
        return default_formatter(value, row, column, data);
    }
};
	

