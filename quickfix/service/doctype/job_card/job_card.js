// Copyright (c) 2026, Sowmiya and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Job Card", {
	refresh: function (frm) {
		frm.set_query("assigned_technician", function () {
			return {
				filters: {
					status: "Active",
					specialization: frm.doc.device_type,
				},
			};
		});

		if (frm.doc.status == "In Repair") {
			frm.dashboard.add_indicator("In Repair", "orange");
		} else if (frm.doc.status == "Ready for Delivery") {
			frm.dashboard.add_indicator("Ready for Delivery", "blue");
		} else if (frm.doc.status == "Delivered") {
			frm.dashboard.add_indicator("Delivered", "green");
		} else if (frm.doc.status == "Cancelled") {
			frm.dashboard.add_indicator("Cancelled", "red");
		}
		if (frm.doc.status == "Ready for Delivery" && frm.doc.docstatus == 1) {
			frm.add_custom_button("Mark as Delivered", function () {
				frm.set_value("status", "Delivered");
				frm.save();
			});
		}
		let name = frappe.boot.quickfix_sname;
		if (name) {
			frm.page.set_title(name);
		}
	},
	assigned_technician: function (frm) {
		if (frm.doc.assigned_technician) {
			frappe.db.get_value(
				"Technician",
				frm.doc.assigned_technician,
				"specialization",
				function (r) {
					if (r.specialization && r.specialization != frm.doc.device_type) {
						frappe.msgprint(
							"Warning: Technician specialization does not match Device Type"
						);
					}
				}
			);
		}
	},
});

frappe.realtime.on("job_ready", (data) => {
	console.log("message");
	frappe.show_alert("Publish Realtime ");
});
