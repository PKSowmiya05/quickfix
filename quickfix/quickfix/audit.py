import frappe
from frappe.utils import now


def log_change(doc, method):
	allowed_doctype = [
		"Job Card",
		"Device Type",
		"QuickFix Settings",
		"Part Usage Entry",
		"Spare Part",
		"Technician",
		"Service Invoice",
	]
	if doc.doctype == "Audit Log":
		return
	if doc.doctype not in allowed_doctype:
		return
	d = frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": doc.doctype,
			"document_name": doc.name,
			"actions": method,
			"user": frappe.session.user,
			"timestamp": now(),
		}
	)
	d.insert()
