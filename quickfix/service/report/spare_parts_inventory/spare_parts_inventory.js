// Copyright (c) 2026, Sowmiya and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	filters: [
		{
			fieldname: "device_type",
			label: "Device Type",
			fieldtype: "Link",
			options: "Device Type",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.stock_qty <= data.reorder_level) {
			value = "<span style='background-color:#ffcccc'>" + value + "</span>";
		}
		return value;
	},
};
