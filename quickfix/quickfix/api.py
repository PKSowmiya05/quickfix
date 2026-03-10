import frappe


@frappe.whitelist()
def transfer_technician(job_card, technician):
	doc = frappe.get_doc("Job Card", job_card)
	doc.assigned_technician = technician
	doc.save()


@frappe.whitelist()
def get_status_chart_data():
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

	return {"labels": labels, "datasets": [{"name": "Job Cards", "values": values}]}
