// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Wastage Report"] = {
	"filters": [
		{
			"fieldname": "work_order",
			"label": "Work Order",
			"fieldtype": "Link",
			"options": "Work Order"
		},
		
		{
			"fieldname": "item_code",
			"label": "Item",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date"
		}
	]
};
