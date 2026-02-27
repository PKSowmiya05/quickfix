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
