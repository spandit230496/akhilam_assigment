import frappe
from frappe.model.document import Document

class TimeTrackerSheet(Document):
    def validate(self):
        if not self.employee_id:
            frappe.throw("Please Enter Time Sheet Through Employee Doctype")

    def after_insert(self):
        self.notify_managers()

    def notify_managers(self):
        managers = frappe.get_all("User", fields=["email"], filters={"role": "Time Sheet Manager"})
        
        if managers:
            manager_emails = [manager['email'] for manager in managers]
            frappe.sendmail(
                recipients=manager_emails,
                subject="New Time Sheet Notification",
                message="A new Time Sheet has been entered into the database. Please go and perform the necessary action."
            )
            frappe.msgprint("Time Sheet Manager has been notified")
        else:
            frappe.msgprint("No Time Sheet Manager found to notify.")

    def on_update(self):
        modified=self.workflow_state
        if modified:  
            self.notify_user()

    def notify_user(self):
        user_email = frappe.get_all("User", fields=["email"], filters={"role": "Time Sheet User"})

        print(user_email)

        if user_email:
            user_emails = [email['email'] for email in user_email]  # Use a meaningful variable name
            frappe.sendmail(
                recipients=user_emails,
                subject="Timesheet Status Update",
                message=f"Your Timesheet status has been updated to '{self.workflow_state}'."
            )
            frappe.msgprint("Time Sheet User has been notified")
        else:
            frappe.msgprint("No Time Sheet User found to notify.")
