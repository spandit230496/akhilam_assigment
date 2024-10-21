// Copyright (c) 2024, Sandip Pandit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
    refresh(frm) {
        frm.add_custom_button(__("Add Attendance"), function() {
            if (frm.doc.name) {
                var employeeId = frm.doc.eid; 
                frappe.new_doc('Time Tracker Sheet', {
                    "employee_id": employeeId
                });
            } else {
                frappe.msgprint(__("Please save the employee record before adding attendance."));
            }
        });
    },
});



