import re
from datetime import date

import frappe
from frappe.rate_limiter import rate_limit


@frappe.whitelist()
def transfer_technician(job_card, technician):
	doc = frappe.get_doc("Job Card", job_card)
	doc.assigned_technician = technician
	doc.save()


@frappe.whitelist()
def get_status_chart_data():
	cache_key = "job_card_status_chart_data"

	cached_data = frappe.cache().get_value(cache_key)
	if cached_data:
		return cached_data

	data = frappe.db.sql(
		"""
        SELECT status, COUNT(*) as count
        FROM `tabJob Card`
        GROUP BY status
    """,
		as_dict=True,
	)

	labels = []
	values = []

	for d in data:
		labels.append(d.status)
		values.append(d.count)

	result = {"labels": labels, "datasets": [{"name": "Job Cards", "values": values}]}

	frappe.cache().set_value(cache_key, result, expires_in_sec=300)

	return result


@frappe.whitelist()
def get_job_summary():
	job_card_name = frappe.form_dict.get("job_card_name")

	if not job_card_name:
		frappe.throw("Job Card name is required")

	if not frappe.db.exists("Job Card", job_card_name):
		return {"status": "error", "message": "Job Card not found"}

	job = frappe.get_doc("Job Card", job_card_name)

	summary = {
		"name": job.name,
		"status": job.status,
		"customer_name": job.customer_name,
		"assigned_technician": job.assigned_technician,
		"final_amount": job.final_amount,
	}

	return summary


@frappe.whitelist()
def get_today_date():
	today = date.today()

	return {"today_date": today}


@frappe.whitelist(allow_guest=True)
def get_job_by_phone():
	ip = frappe.local.request_ip
	key = f"rate_limit:{ip}"

	count = frappe.cache().get(key) or 0
	if int(count) >= 5:
		frappe.local.response["http_status_code"] = 429
		return {"error": "Too many requests"}

	frappe.cache().set(key, int(count) + 1, 60)
	return {"success": "Request allowed"}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=10, seconds=60)
def track_job():
	phone = frappe.form_dict.get("customer_phone")

	if not phone:
		frappe.throw("Phone number is required")

	phone = re.sub(r"\D", "", phone)

	phone = phone[:10]

	if len(phone) != 10:
		frappe.throw("Invalid phone number")

	job_exists = frappe.db.exists("Job Card", {"customer_phone": phone})

	if not job_exists:
		return {"message": "No job found"}

	job = frappe.db.get_value("Job Card", {"customer_phone": phone}, ["name", "status"], as_dict=True)

	return job
