import frappe


def send_mail(job_card):
	print("######## EMAIL FUNCTION RUNNING ########")
	frappe.log_error("tttttt")
	doc = frappe.get_doc("Job Card", job_card)
	frappe.sendmail(
		recipients=doc.customer_email, subject="Job Card", message=f"Job Card {doc.name} is ready"
	)


def error_mail():
	x = 10 / 0
	print(x)
