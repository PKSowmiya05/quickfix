# Copyright (c) 2026, Sowmiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SparePart(Document):
	def autoname(self):
		if not self.part_code:
			frappe.throw("part code need to be filled")
		else:
			self.name = self.part_code.upper() + "-" + frappe.model.naming.make_autoname("PART-.YYYY.-.####")

	def validate(self):
		if not (self.selling_price > self.unit_cost):
			frappe.throw("selling price should be greater")
