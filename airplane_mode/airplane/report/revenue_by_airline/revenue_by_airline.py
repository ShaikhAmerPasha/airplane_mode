# Copyright (c) 2025, ameer and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    airlines_data = frappe.db.sql("""
        SELECT 
            airline, 
            SUM(total_amount) AS total_amount
        FROM 
            `tabAirplane Ticket`
        WHERE 
            total_amount > 0
        GROUP BY 
            airline
        ORDER BY 
            total_amount DESC
    """, as_dict=True)

    total_revenue = sum([ticket['total_amount'] for ticket in airlines_data])

    chart = {
        "data": {
            "labels": [ticket['airline'] for ticket in airlines_data],
            "datasets": [{'values': [ticket['total_amount'] for ticket in airlines_data]}],
        },
        "type": 'donut'
    }

    summary = [{
        "value": total_revenue,
        "indicator": "Green" if total_revenue > 0 else "Red",
        "label": "Total Revenue",
        "datatype": "Currency",
        "currency": "INR"
    }]

    columns = [
        {
            'fieldname': 'airline',
            'label': 'Airlines',
            'fieldtype': 'Link',
            'options': 'Airline'
        },
        {
            'fieldname': 'total_amount',
            'label': 'Total Amount',
            'fieldtype': 'Currency'
        }
    ]

    return columns, airlines_data, None, chart, summary
