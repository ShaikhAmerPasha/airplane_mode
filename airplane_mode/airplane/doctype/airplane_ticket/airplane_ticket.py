# Copyright (c) 2025, ameer and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string


class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_addons()
		self.calculate_total()


	def remove_duplicate_addons(self):
		seen = []
		unique = []
		for row in self.add_ons:
			if row.item not in seen:
				seen.append(row.item)
				unique.append(row)
		self.add_ons = unique

	def calculate_total(self):
		addons_total = sum([row.amount for row in self.add_ons])
		self.total_amount = (self.flight_price or 0) + addons_total

	def before_save(self):
		self.seat = self.generate_random_seat()

	def generate_random_seat(self):
		random_integer = random.randint(1,99)
		random_letter = random.choice(string.ascii_uppercase[:5])
		seat_code = f"{random_integer}{random_letter}"
		return seat_code

		
def stop_submit_if_not_boarded(doc, method):
    if doc.status != "Boarded":
        frappe.throw("Cannot submit untill 'Boarded'.")
