frappe.ui.form.on("Opportunity",{
    refresh:function(frm){
         // Don't show button if document not saved
        if (frm.is_new()) return;
        frm.add_custom_button(__("Create Estimation Request"),function(){
            //popup page
            let estimation_popup = new frappe.ui.Dialog({
                title: 'Create Estimation Request',
                fields:[
                    {
                            label: 'Customer',
                            fieldname: 'customer',
                            fieldtype: 'Link',
                            reqd: 1,
                            options:'Customer'
                        },
                    {
                            label: 'Date',
                            fieldname: 'date',
                            fieldtype: 'Date',
                            reqd: 1
                        },
                    {
                            label: 'Product Details',
                            fieldname: 'product_details',
                            fieldtype: 'Small Text',
                            
                        },
                    {
                            label: 'Qty',
                            fieldname: 'qty',
                            fieldtype: 'Int',
                            reqd: 1
                        },
                    {
                            label: 'Description',
                            fieldname: 'description',
                            fieldtype: 'Long Text',
                            reqd: 1
                        },
                    {
                            label: 'Category',
                            fieldname: 'category',
                            fieldtype: 'Select',
                            options:'\nSignage\nFitout\nWoodwork'
                            
                        },
                    {
                            label: 'Cost Breakdown',
                            fieldname: 'cost_breakdown_section',
                            fieldtype: 'Section Break'
                            
                        },
                        {
                            label: 'Raw Material',
                            fieldname: 'raw_material',
                            fieldtype: 'Currency'
                           
                        },
                    {
                            label: 'Labor',
                            fieldname: 'labor',
                            fieldtype: 'Currency'
                            
                        },
                    {
                            label: 'Delivery',
                            fieldname: 'delivery',
                            fieldtype: 'Currency'
                            
                        },
                    {
                            label: 'Operation',
                            fieldname: 'operation',
                            fieldtype: 'Currency'
                           
                        },
                    {
                            label: 'Totals and Notes',
                            fieldname: 'totals_and_notes_section',
                            fieldtype: 'Section Break'
                           
                        },
                    {
                            label: 'Total Cost',
                            fieldname: 'total_cost',
                            fieldtype: 'Currency'
                          
                        },
                    {
                            label: 'Additional Notes',
                            fieldname: 'additional_notes',
                            fieldtype: 'Long Text'
                           
                        },
                    
                    
                
                ],
                primary_action_label:'Create',
                primary_action(values){
                    frappe.call({
                method:"practice_project.custom_code.estimation_request.create_estimation_request",
                args:{

                    opportunity: frm.doc.name,
                    customer: values.customer,
                    date: values.date,
                    product_details: values.product_details,
                    qty: values.qty,
                    description: values.description,
                    category: values.category,
                    raw_material: values.raw_material,
                    labor: values.labor,
                    delivery: values.delivery,
                    operation: values.operation,
                    total_cost: values.total_cost,
                    additional_notes: values.additional_notes
                },
                callback: function(serverReply){
                    if(!serverReply.exc){
                        frappe.msgprint("Estimation Created: " + serverReply.message);
                        console.log(serverReply.message);
                        estimation_popup.hide();
                    }

                }
            });

                }
            });

            estimation_popup.show();
            
        });
    }
}

);