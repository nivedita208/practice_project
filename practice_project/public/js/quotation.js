frappe.ui.form.on("Quotation", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1 || frm.doc.docstatus === 0)  {   // Only show button if Quotation is submitted or draft
            frappe.db.get_value("Customer", frm.doc.customer, "customer_type", (r) => {
                if (r && r.customer_type === "Individual") {
                    frm.add_custom_button(__("Create Sales Invoice"), function() {
                        frappe.call({
                            method: "frappe.model.mapper.make_mapped_doc",
                            args: {
                                method: "erpnext.selling.doctype.quotation.quotation.make_sales_invoice",
                                source_name: frm.doc.name
                            },
                            callback: function(r) {
                                if (r.message) {
                                    var doc = frappe.model.sync(r.message)[0];
                                    frappe.set_route("Form", doc.doctype, doc.name);
                                }
                            }
                        });
                    }, __("Create"));
                }
            });
        }
    }
});
