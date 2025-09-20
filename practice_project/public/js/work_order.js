frappe.ui.form.on("Work Order", {
    refresh: function(frm) {
        frm.add_custom_button(__('Stock Adjustment (Issue)'), function() {
            frappe.call({
                method: "practice_project.custom_code.work_order.make_stock_adjustment",
                args: {
                    work_order: frm.doc.name,
                    purpose: "Material Issue"
                },
                callback: function(r) {
                    if (r.message) {
                        let doc = frappe.model.sync(r.message)[0];
                        frappe.set_route("Form", doc.doctype, doc.name);
                    }
                }
            });
        }, __("Create"));

        frm.add_custom_button(__('Stock Adjustment (Receipt)'), function() {
            frappe.call({
                method: "practice_project.custom_code.work_order.make_stock_adjustment",
                args: {
                    work_order: frm.doc.name,
                    purpose: "Material Receipt"
                },
                callback: function(r) {
                    if (r.message) {
                        let doc = frappe.model.sync(r.message)[0];
                        frappe.set_route("Form", doc.doctype, doc.name);
                    }
                }
            });
        }, __("Create"));
    }
});

