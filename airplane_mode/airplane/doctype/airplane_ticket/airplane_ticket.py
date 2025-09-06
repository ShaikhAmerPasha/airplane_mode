# Copyright (c) 2025, ameer and contributors
# For license information, please see license.txt

import random
import string

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
    def validate(self):
        self.remove_duplicate_addons()
        self.calculate_total()

    def before_insert(self):
        self._enforce_seat_capacity()

    def before_save(self):
        if not self.seat:
            self.seat = self.generate_random_seat()

    def before_submit(self):
        self._enforce_seat_capacity()

        if self.status != "Boarded":
            frappe.throw(_("Only Boarded tickets can be submitted."), frappe.ValidationError)


    def _enforce_seat_capacity(self):
        """Prevent creating/submitting a ticket when airplane capacity for the flight is reached."""
        if not self.flight:
            return

        frappe.db.sql(
            "SELECT name FROM `tabAirplane Flight` WHERE name = %s FOR UPDATE",
            (self.flight,),
        )

        flight = frappe.db.get_value(
            "Airplane Flight", self.flight, ["airplane"], as_dict=True
        )
        if not flight or not flight.airplane:
            frappe.throw(_("Selected flight has no airplane assigned."), frappe.ValidationError)

        capacity = frappe.db.get_value("Airplane", flight.airplane, "capacity")
        if not capacity:
            frappe.throw(
                _("Airplane {0} has no Capacity set.").format(flight.airplane),
                frappe.ValidationError,
            )
            
        filters = {"flight": self.flight, "docstatus": ["<", 2]}
        booked = frappe.db.count("Airplane Ticket", filters=filters)

        if self.name and frappe.db.exists("Airplane Ticket", self.name):
            existing_flight = frappe.db.get_value("Airplane Ticket", self.name, "flight")
            if existing_flight == self.flight:
                booked -= 1

        if booked >= capacity:
            frappe.throw(
                _(
                    "No seats available. Capacity for flight {flight} "
                    "(airplane {airplane}) is {cap}, already booked: {booked}."
                ).format(
                    flight=self.flight,
                    airplane=flight.airplane,
                    cap=capacity,
                    booked=booked,
                ),
                frappe.ValidationError,
            )

    def remove_duplicate_addons(self):
        seen = set()
        unique_rows = []
        for row in (self.add_ons or []):
            key = row.item
            if key and key not in seen:
                seen.add(key)
                unique_rows.append(row)
        self.set("add_ons", unique_rows)

    def calculate_total(self):
        addons_total = sum((row.amount or 0) for row in (self.add_ons or []))
        self.total_amount = (self.flight_price or 0) + addons_total

    def generate_random_seat(self):
        random_integer = random.randint(1, 99)
        random_letter = random.choice(string.ascii_uppercase[:5])
        return f"{random_integer}{random_letter}"

