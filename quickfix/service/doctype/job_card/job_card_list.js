frappe.listview_settings["Job Card"] = {
	add_fields: ["status", "customer_name", "final_amount", "priority"],
	has_indicator_for_draft: true,
	get_indicator: function (doc) {
		if (doc.status == "In Repair") {
			return ["In Repair", "orange", "status,=,In Repair"];
		}
		if (doc.status == "Ready for Delivery") {
			return ["Ready for Delivery", "blue", "status,=,Ready for Delivery"];
		}

		if (doc.status == "Delivered") {
			return ["Delivered", "green", "status,=,Delivered"];
		}

		if (doc.status == "Cancelled") {
			return ["Cancelled", "red", "status,=,Cancelled"];
		}
	},
	formatters: {
		final_amount(val) {
			return "₹ " + val;
		},
	},
	button: {
		show: function (doc) {
			return doc.status == "In Repair";
		},

		get_label: function () {
			return "Start Repair";
		},
		get_description(doc) {
			return __("View {0}", [`${doc.status}`]);
		},
		action: function (doc) {
			frappe.db.set_value("Job Card", doc.name, "status", "Ready for Delivery").then(() => {
				frappe.msgprint("Status changed to Ready for Delivery for " + doc.name);
				cur_list.refresh();
			});
		},
	},
};
