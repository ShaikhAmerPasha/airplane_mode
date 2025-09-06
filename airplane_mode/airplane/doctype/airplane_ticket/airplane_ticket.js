// Copyright (c) 2025, ameer and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Ticket', {
    refresh(frm) {
        frm.add_custom_button('Assign Seat', () => {
            const d = new frappe.ui.Dialog({
                title: 'Assign Seat',
                fields: [
                    {
                        fieldname: 'seat_input',
                        label: 'Seat Number',
                        fieldtype: 'Data',
                        reqd: 1,
                    }
                ],
                primary_action_label: 'Set Seat',
                primary_action: () => {
                    const seat = (d.get_value('seat_input') || '').toString().trim();
                    if (!seat) {
                        frappe.msgprint('Please enter a seat number.');
                        return;
                    }
                    frm.set_value('seat', seat);
                    d.hide();
                    frappe.show_alert({message: `Seat set to ${seat}`, indicator: 'green'});
                }
            });
            d.show();
        });
    }
});

