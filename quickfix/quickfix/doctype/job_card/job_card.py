# Copyright (c) 2026, Sowmiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		if self.customer_phone and len(self.customer_phone) != 10:
			frappe.throw("Enter a valid phone number")
		if (
			self.status in ["In Repair", "Ready for Delivery", "Delivered", "Cancelled"]
			and not self.assigned_technician
		):
			frappe.throw("Tecnician must exist")
		for i in self.parts_used:
			i.total_price = i.quantity * i.unit_price
		total = 0
		for i in self.parts_used:
			total += i.total_price
		self.parts_total = total
		labour = frappe.get_single_value("QuickFix Settings", "default_labour_charge")
		self.labour_charge = labour
		self.final_amount = self.parts_total + self.labour_charge

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw("Cannot be submitted if status is not ready for delivery")
		for i in self.parts_used:
			stock = frappe.db.get_value("Spare Part", i.part, "stock_quantity")
			if stock < i.quantity:
				frappe.throw(f"Insufficient Quantity {i.part}")

	def on_submit(self):
		for i in self.parts_used:
			stock = frappe.db.get_value("Spare Part", i.part, "stock_quantity")
			new_stock = stock - i.quantity
			frappe.db.set_value("Spare Part", i.part, "stock_quantity", new_stock)
		# here we can bypass the ignore permissions because the deduction of the stock quantity is not manually reduced by the user it is systematically reduced and can ignore the user permissions

		doc = frappe.get_doc(
			{
				"doctype": "Service Invoice",
				"job_card": self.name,
				"customer_name": self.customer_name,
				"invoice_date": frappe.utils.today(),
				"labour_charge": self.labour_charge,
				"parts_total": self.parts_total,
				"total_amount": self.final_amount,
				"payment_status": self.payment_status,
			}
		)
		doc.insert(ignore_permissions=True)
		frappe.publish_realtime(
			"job_ready",
			message={"job_card": self.name, "customer_name": self.customer_name, "status": self.status},
			user=self.owner,
		)
