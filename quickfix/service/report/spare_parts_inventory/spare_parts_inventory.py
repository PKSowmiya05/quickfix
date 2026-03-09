# Copyright (c) 2026, Sowmiya and contributors
# For license information, please see license.txt

# Copyright (c) 2026, Sowmiya and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	total_parts = len(data)
	below_reorder = 0
	total_value = 0
	total_stock = 0

	for d in data:
		stock_qty = d.get("stock_quantity") or 0
		reorder_level = d.get("reorder_level") or 0
		unit_cost = d.get("unit_cost") or 0

		if stock_qty <= reorder_level:
			below_reorder += 1

		value = stock_qty * unit_cost
		total_value += value
		total_stock += stock_qty

	report_summary = [
		{"label": "Total Parts", "value": total_parts, "indicator": "Blue"},
		{"label": "Below Reorder", "value": below_reorder, "indicator": "Red"},
		{
			"label": "Total Inventory Value",
			"value": total_value,
			"indicator": "Green",
			"datatype": "Currency",
		},
	]

	return columns, data, None, None, report_summary


def get_columns():
	return [
		{"label": "Part Name", "fieldname": "part_name", "fieldtype": "Data", "width": 150},
		{"label": "Part Code", "fieldname": "part_code", "fieldtype": "Data", "width": 120},
		{
			"label": "Compatible Device Type",
			"fieldname": "compatible_device_type",
			"fieldtype": "Link",
			"options": "Device Type",
			"width": 130,
		},
		{"label": "Stock Qty", "fieldname": "stock_quantity", "fieldtype": "Int", "width": 100},
		{"label": "Reorder Level", "fieldname": "reorder_level", "fieldtype": "Int", "width": 120},
		{"label": "Unit Cost", "fieldname": "unit_cost", "fieldtype": "Currency", "width": 110},
		{"label": "Selling Price", "fieldname": "selling_price", "fieldtype": "Currency", "width": 120},
		{"label": "Margin %", "fieldname": "margin", "fieldtype": "Percent", "width": 100},
	]


def get_data(filters):
	conditions = {}

	if filters and filters.get("device_type"):
		conditions["compatible_device_type"] = filters.get("device_type")

	parts = frappe.get_list(
		"Spare Part",
		filters=conditions,
		fields=[
			"part_name",
			"part_code",
			"compatible_device_type",
			"stock_quantity",
			"reorder_level",
			"unit_cost",
			"selling_price",
		],
	)

	data = []

	for p in parts:
		margin = 0
		if p.selling_price:
			margin = ((p.selling_price - p.unit_cost) / p.selling_price) * 100

		row = {
			"part_name": p.part_name,
			"part_code": p.part_code,
			"device_type": p.device_type,
			"stock_qty": p.stock_quantity,
			"reorder_level": p.reorder_level,
			"unit_cost": p.unit_cost,
			"selling_price": p.selling_price,
			"margin": margin,
		}

		data.append(row)

	return data
