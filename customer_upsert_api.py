import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def create_or_update_customer(data):
    customer_data = frappe.parse_json(data)
    
    required_fields = ["customer_name", "mobile_number", "address_line1", "city", "pincode", "state", "country"]
    for field in required_fields:
        if field not in customer_data or not customer_data[field]:
            return {"status": "error", "message": f"{field} is required."}, 400
    
    current_user = frappe.session.user
    frappe.set_user("Administrator")
    
    try:
        customer = frappe.get_all("Customer", filters={"mobile_number": customer_data["mobile_number"]}, limit=1)
        
        if customer:
            customer_doc = frappe.get_doc("Customer", customer[0].name)
            for key, value in customer_data.items():
                customer_doc.set(key, value)
            customer_doc.save()
            return {"status": "success", "message": "Customer updated successfully.", "customer_id": customer_doc.name}, 200
        else:
            customer_doc = frappe.new_doc("Customer")
            for key, value in customer_data.items():
                customer_doc.set(key, value)
            customer_doc.insert()
            return {"status": "success", "message": "Customer created successfully.  ", "customer_id": customer_doc.name}, 201
    finally:
        frappe.set_user(current_user)

