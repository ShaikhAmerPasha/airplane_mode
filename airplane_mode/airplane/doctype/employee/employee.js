// Copyright (c) 2025, ameer and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee', {
    before_save: function(frm) {
        if (!frm.doc.title) {
            frm.set_value('title', frm.doc.employee);
        }
    }
});
