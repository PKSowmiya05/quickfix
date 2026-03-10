import frappe
from frappe.utils import today


def test_failed_job():
	raise Exception("This is a test failure for background job")


def check_low_stock():
	# Idempotency guard
	last_run = frappe.db.get_value("Audit Log", {"action": "low_stock_check", "date": today()}, "name")

	if last_run:
		return

	frappe.log_error("Running daily low stock check")

	items = frappe.get_all(
		"Spare Part", filters={"stock_quantity": ["<", 5]}, fields=["part_name", "stock_quantity"]
	)

	for item in items:
		frappe.log_error(f"Low stock item: {item.part_name}")


def generate_monthly_revenue_report():
	frappe.log_error("Generating monthly revenue report")

	total = frappe.db.sql("""
        SELECT SUM(final_amount)
        FROM `tabJob Card`
        WHERE status='Delivered'
    """)

	frappe.log_error(f"Monthly revenue: {total}")
