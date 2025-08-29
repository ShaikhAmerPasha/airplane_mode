import frappe, random

def execute():
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"seat": ["in", ["", None]]},
        pluck="name"
    )

    for name in tickets:
        seat = f"{random.randint(1, 99)}{random.choice(['A','B','C','D','E'])}"
        frappe.db.set_value("Airplane Ticket", name, "seat", seat, update_modified=False)