# Copyright (c) 2026, Sowmiya and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


def create_technician():
	exist = frappe.db.exists(
		"Technician",
		{
			"technician_name": "test",
			"phone": "9887654321",
		},
	)
	if exist:
		return frappe.get_doc("Technician", exist)
	doc = frappe.get_doc(
		{
			"doctype": "Technician",
			"technician_name": "test",
			"phone": "9887654321",
		}
	)
	doc.insert()
	return doc


def create_spare_part():
	exist = frappe.db.exists(
		"Spare Part",
		{
			"part_code": "SM-001",
			"part_name": "test part",
			"unit_cost": 6,
			"selling_price": 50,
			"stock_quantity": 8,
		},
	)
	if exist:
		return frappe.get_doc("Spare Part", exist)
	doc = frappe.get_doc(
		{
			"doctype": "Spare Part",
			"part_code": "SM-001",
			"part_name": "test part",
			"unit_cost": 6,
			"selling_price": 50,
			"stock_quantity": 8,
		}
	)
	doc.insert()
	return doc


def create_device_type():
	exist = frappe.db.exists(
		"Device Type",
		{
			"device_type": "test device",
		},
	)
	if exist:
		return frappe.get_doc("Device Type", exist)
	doc = frappe.get_doc(
		{
			"doctype": "Device Type",
			"device_type": "test device",
		}
	)
	doc.insert()

	return doc


def create_job_card(**args):
	print("args", args)
	tech = create_technician()
	device = create_device_type()
	spare_part = create_spare_part()

	exist = frappe.db.exists(
		"Job Card",
		{
			"customer_name": args.get("customer_name") or "test customer",
			"customer_phone": args.get("customer_phone") or "7896541235",
			"device_type": device.name,
			"assigned_technician": tech.name,
		},
	)
	if exist:
		return frappe.get_doc("Job Card", exist)
	doc = frappe.get_doc(
		{
			"doctype": "Job Card",
			"customer_name": args.get("customer_name") or "test customer",
			"customer_phone": args.get("customer_phone") or "7896541235",
			"device_type": device.name,
			"assigned_technician": tech.name,
			"problem_description": "To test the device",
			"parts_used": [
				{
					"part": spare_part.name,
					"part_name": spare_part.part_name,
					"quantity": float(args.get("quantity") or 0) or 2,
					"unit_price": float(args.get("unit_price") or 0) or spare_part.selling_price,
				}
			],
		}
	)
	print(doc.as_dict())
	doc.insert()
	return doc


class TestJobCard(FrappeTestCase):
	def setUp(self):
		self.device = create_device_type()
		self.tech = create_technician()
		self.spare = create_spare_part()
		args = {
			"customer_name": "Sowmiya",
			"customer_phone": "7894561234",
			"quantity": "2",
			"unit_price": "50",
		}
		self.job_card = create_job_card(**args)

	# def test_job_card_create(self):
	#     self.assertEqual(self.job_card.docstatus,0)
	# def test_phone_short(self):
	#      with self.assertRaises(frappe.ValidationError):
	#         create_job_card(customer_phone="12345")

	# def test_phone_long(self):
	#      with self.assertRaises(frappe.ValidationError):
	#         create_job_card(customer_phone="1234567891011")
	# def test_phone_non_numeric(self):
	#     with self.assertRaises(frappe.ValidationError):
	#         create_job_card(customer_phone="98AB654321")
	# def test_valid_phone(self):
	#     doc = create_job_card(customer_phone="9876543210")
	#     self.assertEqual(doc.customer_phone, "9876543210")
	def test_job_card_calculations(self):
		doc = create_job_card(quantity="2", unit_price="50")

		print(doc.parts_total)
		self.assertEqual(doc.parts_total, 100)
		print(doc.final_amount)
		self.assertEqual(doc.final_amount, 600)

	def tearDown(self):
		frappe.db.rollback()
