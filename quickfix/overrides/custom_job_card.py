import frappe

from quickfix.service.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):
	def validate(self):
		super().validate()  # ALWAYS call super first
		self._check_urgent_unassigned()

	def _check_urgent_unassigned(self):
		if self.priority == "Urgent" and not self.assigned_technician:
			settings = frappe.get_single("QuickFix Settings")
			frappe.enqueue(
				"quickfix.utils.send_urgent_alert", job_card=self.name, manager=settings.manager_email
			)


# Method Resolution Order (MRO) defines the order in which Python searches for a method in a class and its parent classes.
# When a method like validate(), on_submit(), or save() runs, Python follows the MRO to decide which method to execute.

# super() is non-negotiable because super helps to execute the parent class methods and aslo executes the overrided doctype class

# override_doctype method is used to change the core behaviour of the doctype while the doc_events is used to add or change functionalities like validate or submit
# override_doctype method is chosen over_doc events when full control over the doctype is required


def install():
	device = ["Smart Phone", "Laptop", "Tablet"]
	for d in device:
		if not frappe.db.exists("Device Type", d):
			doc = frappe.get_doc({"doctype": "Device Type", "device_type": d})
			doc.insert()
	if not frappe.db.exists("QuickFix Settings"):
		doc = frappe.get_doc(
			{
				"doctype": "QuickFix Settings",
				"default_labour_charge": 600,
				"manager_email": "karthisowmiya05@gmail.com",
			}
		)
		doc.insert()

	print("QuickFix setup completed successfully")


def uninstall():
	if frappe.db.exists("Job Card", {"docstatus": 1}):
		raise frappe.ValidationError("Submittable doctype exist")


def extend_bootinfo(bootinfo):
	s = frappe.get_single("QuickFix Settings")
	bootinfo.quickfix_sname = s.shop_name
	bootinfo.quickfix_memail = s.manager_email


def login(login_manager):
	frappe.log_error(title="User Login", message=f"{frappe.session.user} logged in successfully")


def logout(login_manager):
	frappe.log_error(title="User logged out", message=f"{frappe.session.user} logged out successfully")


def get_shop_name():
	setting = frappe.get_single("QuickFix Settings")
	return setting.shop_name


def format_job_id(value):
	return f"JOB#{value}"
