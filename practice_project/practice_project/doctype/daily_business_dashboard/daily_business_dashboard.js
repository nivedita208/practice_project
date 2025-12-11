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
                    let html = dashboard_content(r.message);
                    frm.fields_dict.dashboard.$wrapper.html(html);
                }
            }
        });
    }
});

function dashboard_content(data) {

    let so = data.so_list;
    let si = data.si_list;
    let q = data.q_list;

    let html = `
        <style>
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 10px;
            font-family: Arial, sans-serif;
        }
        .dashboard-card {
            padding: 18px;
            border-radius: 12px;
            color: #fff;
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card-so { background: #4c6ef5; }
        .card-si { background: #2eb85c; }
        .card-q  { background: #f59f00; }
        .card-ev { background: #e64980; }
        .dashboard-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }
        .dashboard-number {
            font-size: 26px;
            font-weight: bold;
            margin-top: 10px;
        }
        h4 {
            margin-top: 20px;
            margin-bottom: 10px;
        }
        table {
            width: 80%;
            border-collapse: collapse;
            margin-top: 15px;
            margin-bottom: 25px;
            font-size: 13px;
        }
        th {
            background: #ffe6e6;
            font-weight: 800;
            color: black;
            padding: 8px;
            border-bottom: 2px solid #ddd;
        }
        td {
            padding: 8px;
            border-bottom: 1px solid #eee;
        }
       
        </style>

        <div class="dashboard-title">Daily Dashboard</div>

        <div class="dashboard-grid">
            <div class="dashboard-card card-so">
                Sales Orders
                <div class="dashboard-number">${data.sales_orders}</div>
            </div>

            <div class="dashboard-card card-q">
                Quotations
                <div class="dashboard-number">${data.quotations}</div>
            </div>

            <div class="dashboard-card card-si">
                Sales Invoices
                <div class="dashboard-number">${data.sales_invoices}</div>
            </div>

            <div class="dashboard-card card-ev">
                Meetings
                <div class="dashboard-number">${data.events}</div>
            </div>
        </div>

        <!-- SI table -->
        <h4>Sales Invoice</h4>
        <table>
            <tr><th>Name</th><th>Date</th></tr>
            ${si.map(s => `
                <tr>
                    <td>${s.name}</td>
                    <td>${s.posting_date}</td>
                </tr>
            `).join("")}
        </table>

        <!-- SO table -->
        <h4>Sales Order </h4>
        <table>
            <tr><th>Name</th><th>Date</th></tr>
            ${so.map(ss => `
                <tr>
                    <td>${ss.name}</td>
                    <td>${ss.transaction_date}</td>
                </tr>
            `).join("")}
        </table>

        <!-- Quotation table -->
        <h4>Quotation </h4>
        <table>
            <tr><th>Name</th><th>Date</th></tr>
            ${q.map(qq => `
                <tr>
                    <td>${qq.name}</td>
                    <td>${qq.transaction_date}</td>
                </tr>
            `).join("")}
        </table>
    `;

    return html;
}


// pending task : add css to cards and inject 4 tables so,si,qo,events