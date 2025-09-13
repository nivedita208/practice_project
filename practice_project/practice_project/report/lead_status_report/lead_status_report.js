// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Status Report"] = {
	"filters": [
		{ "fieldname": "from_date", "label": "From Date", "fieldtype": "Date" },
        { "fieldname": "to_date", "label": "To Date", "fieldtype": "Date" },
        { "fieldname": "source", "label": "Lead Source", "fieldtype": "Link", "options": "Lead Source" },
        { "fieldname": "lead_owner", "label": "Lead Owner", "fieldtype": "Link", "options": "User" }
	]
};
