// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Efficiency Report"] = {
	"filters": [
		{ "fieldname": "from_date", "label": "From Date", "fieldtype": "Date" },
        { "fieldname": "to_date", "label": "To Date", "fieldtype": "Date" },
        { "fieldname": "source", "label": "Lead Source", "fieldtype": "Link", "options": "Lead Source" },
        { "fieldname": "owner", "label": "Lead Owner", "fieldtype": "Link", "options": "User" }
	]
};
