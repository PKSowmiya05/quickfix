import frappe


def get_context(context):
	job_id = frappe.form_dict.get("job_id")

	if job_id:
		job = frappe.db.get_value("Job Card", job_id, ["name", "status", "device_name"], as_dict=True)

		context.job = job

	context.title = "Track My Job"
	context.description = "Track your device repair status online"
	context.og_title = "Track Job Status"
