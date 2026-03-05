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
			frappe.show_alert("Repair Started");
		}
		if (!frappe.user.has_role("QF Manager")) {
			frm.set_df_property("customer_phone", "hidden", 1);
		}

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
		frm.add_custom_button("Transfer Technician", function () {
			frappe.prompt(
				{
					label: "New Technician",
					fieldname: "new_technician",
					fieldtype: "Link",
					options: "Technician",
				},
				function (values) {
					frappe.confirm("Are you sure you want to transfer technician?", function () {
						frappe.call({
							method: "quickfix.quickfix.api.transfer_technician",
							args: {
								job_card: frm.doc.name,
								technician: values.new_technician,
							},
							callback: function () {
								frm.set_value("assigned_technician", values.new_technician);
								frm.trigger("assigned_technician");
								frm.save();
							},
						});
					});
				}
			);
		});
		frm.add_custom_button("Reject Job", function () {
			let d = new frappe.ui.Dialog({
				title: "Reject Job",
				fields: [
					{
						label: "Rejection Reason",
						fieldname: "reason",
						fieldtype: "Small Text",
						reqd: 1,
					},
				],
				primary_action_label: "Submit",
				primary_action(values) {
					frm.set_value("status", "Cancelled");
					frm.save();
					d.hide();
				},
			});

			d.show();
		});
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

	onload: function (frm) {
		frappe.realtime.on("job_ready", function (data) {
			frappe.show_alert({
				message: "Job Ready",
				indicator: "blue",
			});
		});
	},
});

frappe.ui.form.on("Part Usage Entry", {
	quantity: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		let total = (row.quantity || 0) * (row.unit_price || 0);
		frappe.model.set_value(cdt, cdn, "total_price", total);
	},
});
