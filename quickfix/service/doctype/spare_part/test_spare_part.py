# Copyright (c) 2026, Sowmiya and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


def create_spare_part(**args):
	doc = frappe.get_doc(
		{
			"doctype": "Spare Part",
			"part_code": args.get("part_code") or "SM-001",
			"part_name": args.get("part_name") or "test part",
			"unit_cost": args.get("unit_cost") or 10,
			"selling_price": args.get("selling_price") or 20,
			"stock_quantity": 5,
		}
	)

	doc.insert()
	return doc


class TestSparePart(FrappeTestCase):
	def test_selling_price_less_than_cost(self):
		with self.assertRaises(frappe.ValidationError):
			create_spare_part(unit_cost=10, selling_price=9)

	def test_selling_price_equal_cost(self):
		with self.assertRaises(frappe.ValidationError):
			create_spare_part(unit_cost=10, selling_price=10)

	def test_selling_price_valid(self):
		doc = create_spare_part(unit_cost=10, selling_price=11)
		self.assertEqual(doc.selling_price, 11)

	def tearDown(self):
		frappe.db.rollback()
