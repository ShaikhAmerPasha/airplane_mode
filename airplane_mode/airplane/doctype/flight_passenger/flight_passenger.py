# Copyright (c) 2025, ameer and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		parts = [self.first_name, self.last_name]
		self.full_name = " ".join(p for p in parts if p).strip()
