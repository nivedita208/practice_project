// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Business Dashboard", {
    refresh(frm) {
        
        frm.trigger("load_dashboard");
    },

    from_date(frm) {
        frm.trigger("load_dashboard");
    },

    to_date(frm) {
        frm.trigger("load_dashboard");
    },

    load_dashboard(frm) {
        if (!frm.doc.from_date || !frm.doc.to_date) return;

        frappe.call({
            method: "practice_project.practice_project.doctype.daily_business_dashboard.daily_business_dashboard.get_dashboard_data",
            args: {
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date
            },
            callback: function(r) {
                if (r.message) {
					console.log("kitty",r);
					console.log("hello meow",r.message);
				let	data = r.message;

				let html = `
				<div>
				 <h3>Daily Dashboard</h3>
                <p><b>Sales Orders:</b> ${data.sales_orders}</p>
                <p><b>Quotations:</b> ${data.quotations}</p>
                <p><b>Sales Invoices:</b> ${data.sales_invoices}</p>
                <p><b>Meetings:</b> ${data.events}</p>
				</div>

				`;
				frm.fields_dict.dashboard.$wrapper.html(html);
                    
                }
            }
        });

        
    }
});


// pending task : add css to cards and inject 4 tables so,si,qo,events