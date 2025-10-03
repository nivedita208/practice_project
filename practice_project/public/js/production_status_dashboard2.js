frappe.ui.form.on('Production Status Dashboard2', {
  refresh: function(frm) {
      if (!frm.doc.cost_center) {
          frm.fields_dict.dashboard_html.$wrapper.html(
              "<div class='text-muted'>Select a Cost Center to view the dashboard</div>"
          );
          return;
      }
      load_dashboard(frm);   // Initial dashboard load
      start_auto_refresh(frm); // Auto-refresh every 20 seconds

      // Add Refresh button
      frm.add_custom_button(__('Refresh Dashboard'), () => {
          load_dashboard(frm);
      });
  },
  cost_center: load_dashboard
});

function load_dashboard(frm) {
  if (!frm.doc.cost_center) return;
  frm.fields_dict.dashboard_html.$wrapper.html("Loading...");

  frappe.call({
      method: "practice_project.custom_code.production_status_dashboard2.get_dashboard_data",
      args: { cost_center: frm.doc.cost_center },
      callback: function(r) {
          if (r.message) {
              let html = render_dashboard(r.message, frm);
              frm.fields_dict.dashboard_html.$wrapper.html(html);
          }
      }
  });
}

// Map status to CSS class for table badges
function getStatusClass(status) {
    status = status.toLowerCase();
    if (status === "not started" || status === "open") return "status-pending";       // Gray
    if (status === "in process" || status === "work in progress") return "status-in-process"; // Blue
    if (status === "on hold") return "status-on-hold";      // Amber
    if (status === "overdue") return "status-overdue";      // Red
    if (status === "completed today" || status === "completed") return "status-completed-today"; // Green
    return "status-pending"; // fallback
}

// Map KPI type to class
function getKpiClass(type) {
    switch(type) {
        case "pending": return "kpi-pending";
        case "in_process": return "kpi-in-process";
        case "on_hold": return "kpi-on-hold";
        case "overdue": return "kpi-overdue";
        case "completed_today": return "kpi-completed-today";
        default: return "kpi-pending";
    }
}

function render_dashboard(data, frm) {
  let k = data.kpis;
  let wo = data.work_orders || [];
  let jc = data.job_cards || [];

  let html = `
  <style>
    /* KPI Cards */
    .kpi-card { border-radius: 12px; padding: 20px; margin: 8px; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); color: #fff; font-weight: 600;
        transition: transform 0.25s, box-shadow 0.25s; }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 6px 16px rgba(0,0,0,0.15); }
    .kpi-value { font-size: 28px; font-weight: 700; margin-bottom: 6px; }
    .kpi-label { font-size: 14px; color: rgba(255,255,255,0.9); font-weight: 500; }

    h4 { margin-top: 20px; margin-bottom: 10px; }

    table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; font-size: 13px;
        background: var(--bg-color); color: var(--text-color); }
    th { background: var(--control-bg); color: var(--text-color); font-weight: 600; padding: 8px;
        border-bottom: 2px solid var(--border-color); }
    td { padding: 8px; border-bottom: 1px solid var(--border-color); }
    tr:hover { background: var(--hover-color); }

    /* Status badges */
    .status-badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 11px;
        color: #fff; font-weight: 600; }
    .status-pending { background: #6c757d; }       /* Gray */
    .status-in-process { background: #007bff; }    /* Blue */
    .status-on-hold { background: #ffbf00; }       /* Amber */
    .status-overdue { background: #dc3545; }       /* Red */
    .status-completed-today { background: #28a745; } /* Green */

    /* KPI colors: light theme */
    html[data-theme="light"] .kpi-pending { background: #6c757d; }
    html[data-theme="light"] .kpi-in-process { background: #0d6efd; }
    html[data-theme="light"] .kpi-on-hold { background: #ffbf00; }
    html[data-theme="light"] .kpi-overdue { background: #dc3545; }
    html[data-theme="light"] .kpi-completed-today { background: #28a745; }

    /* KPI colors: dark theme */
    html[data-theme="dark"] .kpi-pending { background: #495057; }
    html[data-theme="dark"] .kpi-in-process { background: #339af0; }
    html[data-theme="dark"] .kpi-on-hold { background: #ffb703; }
    html[data-theme="dark"] .kpi-overdue { background: #ff6b6b; }
    html[data-theme="dark"] .kpi-completed-today { background: #51cf66; }
  </style>

  <!-- KPI Cards -->
  <div class="row">
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('pending')}"><div class="kpi-value">${k.pending_wos}</div><div class="kpi-label">Pending WOs</div></div></div>
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('in_process')}"><div class="kpi-value">${k.in_process_wos}</div><div class="kpi-label">In Process WOs</div></div></div>
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('overdue')}"><div class="kpi-value">${k.overdue_wos}</div><div class="kpi-label">Overdue WOs</div></div></div>
    ${frm.doc.show_completed_today == 1 ? `
      <div class="col-sm-3"><div class="kpi-card ${getKpiClass('completed_today')}"><div class="kpi-value">${k.completed_today_wos}</div><div class="kpi-label">Completed Today WOs</div></div></div>
     ` : ''}
     
  </div>

  <div class="row">
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('pending')}"><div class="kpi-value">${k.pending_jcs}</div><div class="kpi-label">Pending JCs</div></div></div>
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('in_process')}"><div class="kpi-value">${k.in_process_jcs}</div><div class="kpi-label">In Process JCs</div></div></div>
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('on_hold')}"><div class="kpi-value">${k.on_hold_jcs}</div><div class="kpi-label">On Hold JCs</div></div></div>
    <div class="col-sm-3"><div class="kpi-card ${getKpiClass('overdue')}"><div class="kpi-value">${k.overdue_jcs}</div><div class="kpi-label">Overdue JCs</div></div></div>
    ${frm.doc.show_completed_today == 1 ? `
      <div class="col-sm-3"><div class="kpi-card ${getKpiClass('completed_today')}"><div class="kpi-value">${k.completed_today_jcs}</div><div class="kpi-label">Completed Today JCs</div></div></div>
     ` : ''}
     
  </div>

  <!-- Work Orders Table -->
  <h4>Work Orders</h4>
  <table>
    <tr>
      <th>Work Order</th><th>Production Item</th><th>Req Qty</th><th>Produced Qty</th>
      <th>Status</th><th>Planned Start Date</th><th>Planned End Date</th>
    </tr>
    ${wo.map(w => {
        let woStatus = w.status;
        if (w.planned_end_date && new Date(w.planned_end_date) < new Date() && w.status !== "Completed") {
            woStatus = "Overdue";
        }
        if (woStatus === "Completed" && k.completed_today_wos) woStatus = "Completed Today";
        return `<tr>
          <td><a href="#Form/Work Order/${w.name}">${w.name}</a></td>
                    <td>${w.production_item || ""}</td>
          <td>${w.qty || ""}</td>
          <td>${w.produced_qty || ""}</td>
          <td><span class="status-badge ${getStatusClass(woStatus)}">${woStatus}</span></td>
          <td>${w.planned_start_date || ""}</td>
          <td>${w.planned_end_date || ""}</td>
        </tr>`;
    }).join("")}
  </table>

  <!-- Job Cards Table -->
  <h4>Job Cards</h4>
  <table>
    <tr>
      <th>Job Card</th><th>Work Order</th><th>Operation</th><th>Work Station</th>
      <th>Qty</th><th>Status</th><th>Expected Start Date</th><th>Expected End Date</th>
    </tr>
    ${jc.map(j => {
        let jcStatus = j.status;
        if (j.expected_end_date && new Date(j.expected_end_date) < new Date() && j.status !== "Completed") {
            jcStatus = "Overdue";
        }
        if (jcStatus === "Completed" && k.completed_today_jcs) jcStatus = "Completed Today";
        return `<tr>
          <td><a href="#Form/Job Card/${j.name}">${j.name}</a></td>
          <td>${j.work_order || ""}</td>
          <td>${j.operation || ""}</td>
          <td>${j.workstation || ""}</td>
          <td>${j.for_qty || ""}</td>
          <td><span class="status-badge ${getStatusClass(jcStatus)}">${jcStatus}</span></td>
          <td>${j.expected_start_date || ""}</td>
          <td>${j.expected_end_date || ""}</td>
        </tr>`;
    }).join("")}
  </table>
  `;

  return html;
}

// Auto-refresh function
function start_auto_refresh(frm) {
    if (frm.auto_refresh_interval) return; // Prevent multiple intervals
    frm.auto_refresh_interval = setInterval(() => {
        frm.reload_doc();
    }, 20000); // 20 seconds
}

