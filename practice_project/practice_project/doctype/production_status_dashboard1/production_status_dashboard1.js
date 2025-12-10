// Copyright (c) 2025, Nivedita and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Status Dashboard1', {
	 refresh: function(frm) {
// why to use this refresh , why to call  auto_refresh_form(frm); inside this?
		load_dashboard1(frm);
		auto_refresh_form(frm);

		frm.add_custom_button(__('Refresh'),function(){
			//page should be refreshed
		}		
	)
	 },
	 // This function runs automatically whenever the 'cost_center' field value changes
  cost_center: function(frm) {
      // Call the load_dashboard function to refresh the dashboard data
      load_dashboard(frm);
  }
});

// connect backend to frontend
function load_dashboard1(frm){
	frappe.call({
		method:"",
		args:{},
		callback:function(response){
			//add repsonse message here
			// add reload doc
			let html = render_dashboard(r.message, frm); // what this will do ?
              frm.fields_dict.dashboard_html.$wrapper.html(html); 
		}
	})

}
// calling render_dashboard inside the load_dashboard and load_dashboard above 

function render_dashboard1(data){
	// format data in html style
	let k = data.kpis ;
	let wo = data.work_orders || [] ;
	let jc = data.jcs || [] ;

	let html = `
	<style>
	// css code 
	</style>
	 <!-- KPI Cards wo& jcs -->

	<!-- Work Orders Table use .map() & .join() -->
	<!-- job card Table	.map() & .join() -->
	
	`;

	return html;
}

// add timer reload 
function auto_refresh_form(frm){
	frm.auto_refresh_interval = setInterval(function(){
		//it reload the doc each evry 60secs
		frm.reload_doc();
	},60000);

}




