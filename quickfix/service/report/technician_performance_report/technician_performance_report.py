import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	report_summary = get_report_summary(data)
	return columns, data, None, chart, report_summary


def get_columns():
	columns = [
		{
			"label": "Technician",
			"fieldname": "technician",
			"fieldtype": "Link",
			"options": "Technician",
			"width": 150,
		},
		{"label": "Total Jobs", "fieldname": "total_jobs", "fieldtype": "Int", "width": 120},
		{"label": "Completed", "fieldname": "completed", "fieldtype": "Int", "width": 120},
		{"label": "Avg Turnaround Days", "fieldname": "avg_turnaround", "fieldtype": "Float", "width": 180},
		{"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 120},
		{"label": "Completion Rate %", "fieldname": "completion_rate", "fieldtype": "Percent", "width": 150},
	]

	device_types = frappe.db.sql(
		"""
        SELECT DISTINCT device_type FROM `tabJob Card`
    """,
		as_dict=True,
	)

	for d in device_types:
		if d.device_type:
			columns.append(
				{
					"label": d.device_type,
					"fieldname": d.device_type.lower().replace(" ", "_"),
					"fieldtype": "Int",
					"width": 120,
				}
			)

	return columns


def get_data(filters):
	conditions = ""
	values = {}

	if filters.get("from_date"):
		conditions += " AND creation >= %(from_date)s"
		values["from_date"] = filters.get("from_date")

	if filters.get("to_date"):
		conditions += " AND creation <= %(to_date)s"
		values["to_date"] = filters.get("to_date")

	if filters.get("technician"):
		conditions += " AND assigned_technician = %(technician)s"
		values["technician"] = filters.get("technician")

	jobs = frappe.db.sql(
		f"""
        SELECT assigned_technician, device_type, status, final_amount, creation, modified
        FROM `tabJob Card`
        WHERE 1=1 {conditions}
    """,
		values,
		as_dict=True,
	)

	device_types = frappe.db.sql(
		"""
        SELECT DISTINCT device_type FROM `tabJob Card`
    """,
		as_dict=True,
	)

	device_types = [d.device_type for d in device_types if d.device_type]

	technician_data = {}

	for job in jobs:
		tech = job.assigned_technician

		if tech not in technician_data:
			technician_data[tech] = {
				"technician": tech,
				"total_jobs": 0,
				"completed": 0,
				"revenue": 0,
				"total_days": 0,
			}

			for device in device_types:
				field = device.lower().replace(" ", "_")
				technician_data[tech][field] = 0

		technician_data[tech]["total_jobs"] += 1

		if job.status == "Delivered":
			technician_data[tech]["completed"] += 1

		technician_data[tech]["revenue"] += job.final_amount or 0

		days = (job.modified - job.creation).days
		technician_data[tech]["total_days"] += days

		if job.device_type:
			field = job.device_type.lower().replace(" ", "_")
			if field in technician_data[tech]:
				technician_data[tech][field] += 1

	data = []

	for tech in technician_data.values():
		avg_turnaround = 0
		completion_rate = 0

		if tech["total_jobs"]:
			avg_turnaround = tech["total_days"] / tech["total_jobs"]
			completion_rate = (tech["completed"] / tech["total_jobs"]) * 100

		row = {
			"technician": tech["technician"],
			"total_jobs": tech["total_jobs"],
			"completed": tech["completed"],
			"avg_turnaround": avg_turnaround,
			"revenue": tech["revenue"],
			"completion_rate": completion_rate,
		}

		for device in device_types:
			field = device.lower().replace(" ", "_")
			row[field] = tech[field]

		data.append(row)

	return data


def get_chart_data(data):
	labels = []
	total_jobs = []
	completed_jobs = []

	for row in data:
		labels.append(row["technician"])
		total_jobs.append(row["total_jobs"])
		completed_jobs.append(row["completed"])

	chart = {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Total Jobs", "values": total_jobs},
				{"name": "Completed Jobs", "values": completed_jobs},
			],
		},
		"type": "bar",
	}

	return chart


def get_report_summary(data):
	total_jobs = 0
	total_revenue = 0
	best_technician = ""
	best_rate = 0

	for row in data:
		total_jobs += row["total_jobs"]
		total_revenue += row["revenue"]

		if row["completion_rate"] > best_rate:
			best_rate = row["completion_rate"]
			best_technician = row["technician"]

	summary = [
		{"label": "Total Jobs", "value": total_jobs, "indicator": "Blue"},
		{"label": "Total Revenue", "value": total_revenue, "indicator": "Green"},
		{"label": "Best Technician", "value": best_technician, "indicator": "Orange"},
	]

	return summary
