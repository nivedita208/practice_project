frappe.listview_settings['Lead'] = {
    add_fields: ["custom_priority_status"],
    get_indicator(doc) {
        if (doc.custom_priority_status === "Fresh") {
            return [__("Fresh"), "green", "custom_priority_status,=,Fresh"];
        } 
        if (doc.custom_priority_status === "Low Priority") {
            return [__("Low Priority"), "grey", "custom_priority_status,=,Low Priority"];
        }
    }
};







