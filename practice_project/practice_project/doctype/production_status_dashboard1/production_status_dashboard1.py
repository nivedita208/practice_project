# Copyright (c) 2025, Nivedita and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProductionStatusDashboard1(Document):
    
	def validate(self):
		# Ensure unique cost_center
		if self.cost_center:
			existing = frappe.db.exists(
				"Production Status Dashboard",
				{"cost_center": self.cost_center, "name": ["!=", self.name]}
			)
		if existing:
			frappe.throw(
				f"A Production Status Dashboard already exists for Cost Center '{self.cost_center}'"
			)

# add code to fetch data from backend jc and wo