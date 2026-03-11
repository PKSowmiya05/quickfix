import frappe
from frappe.utils import today


def test_failed_job():
	raise Exception("This is a test failure for background job")


def check_low_stock():
	# Idempotency guard
	last_run = frappe.db.get_value("Audit Log", {"actions": "low_stock_check", "timestamp": today()}, "name")

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


def cancel_old_draft_job_cards():
	frappe.db.sql("""
        UPDATE `tabJob Card`
        SET status = 'Cancelled'
        WHERE docstatus = 0
        LIMIT 1000
    """)

	frappe.db.commit()


def insert_audit_logs():
	logs = []

	for i in range(500):
		logs.append((f"LOG-{i}", "low_stock_check"))

	frappe.db.bulk_insert("Audit Log", ["name", "actions"], logs)

	frappe.db.commit()
