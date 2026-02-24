import frappe


@frappe.whitelist(allow_guest=True)
def execute():
	return {"name": "Sowmiya"}
