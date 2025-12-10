# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt
import frappe 
from frappe.model.document import Document


class Estimation(Document):                        
    # function for raw material table and operation table             
    
    def duration_to_hours(duration_str):
        days = hours = minutes = seconds = 0

        # Split by space: e.g., "1d 1h 30m"
        parts = str(duration_str).split()

        for part in parts:
            if part.endswith("d"):
                days = int(part[:-1])
            elif part.endswith("h"):
                hours = int(part[:-1])
            elif part.endswith("m"):
                minutes = int(part[:-1])
            elif part.endswith("s"):
                seconds = int(part[:-1])

        total_hours = (days * 24) + hours + (minutes / 60) + (seconds / 3600)
        return total_hours

    def validate(self):
        #  estimation creation(max 2 allowed)
        if self.opportunity:
            existing_estimations = frappe.get_all(
                "Estimation",
                filters={
                    "opportunity": self.opportunity,
                    "docstatus": ["!=", 2]  # ignore Cancelled
                },
                fields=["name","docstatus"]
            )
            
            #initialize counters
            draft_count = 0
            submitted_count = 0
            
             # Count how many drafts and submitted already exist 
            for e in existing_estimations:
                
                if e.name == self.name:
                    continue  # skip current document itself

                if e.docstatus == 0:   # Draft
                    draft_count = draft_count + 1

                if e.docstatus == 1:   # Submitted
                    submitted_count = submitted_count + 1

            if self.docstatus == 0 and draft_count >= 1:
                frappe.throw("Only 1 draft Estimation is allowed per Opportunity")
                
            if self.docstatus == 1 and submitted_count >= 2:
                frappe.throw("Only 2 submitted Estimation are  allowed per Opportunity")
                
                
        # --- Restrict creation without Opportunity ---
        if not self.opportunity:
            frappe.throw("Estimation can only be created from an Opportunity")

        # --- Calculate Raw Material Totals ---
        total_raw_material = 0
        for row in self.eestimation_raw_material:   # child table fieldname
            if row.qty and row.rate:
                row.amount = row.qty * row.rate
                total_raw_material += row.amount

        # --- Calculate Operation Totals (Duration-based) ---
        total_operations = 0
        for row in self.estimation_operation:
            if row.operation_time and row.machine_hour_rate:
                hours = Estimation.duration_to_hours(row.operation_time)
                row.operation_cost = hours * row.machine_hour_rate
                total_operations += row.operation_cost

        self.total_operations_cost = total_operations

        # --- Delivery Charges ---
        delivery = self.delivery_charges or 0

        # --- Final Calculation ---
        subtotal = total_raw_material + total_operations + delivery

        # Apply Profit %
        profit_percentage = self.profit_percentage or 0
        profit_amount = subtotal * (profit_percentage / 100)

        # Final Sales Rate
        self.sales_rate = subtotal + profit_amount

        # Store totals in parent doc
        self.total_raw_material = total_raw_material
        self.total_operations = total_operations
        self.profit_amount = profit_amount
        self.grand_total = self.sales_rate

        # ------------------------------
        # OLD LOGIC (when Time was Float)
        # ------------------------------
        """
        total_operations = 0
        for row in self.estimation_operation:   # child table fieldname
            if row.operation_time and row.machine_hour_rate:
                row.operation_cost = row.operation_time * row.machine_hour_rate
                total_operations += row.operation_cost
        """
