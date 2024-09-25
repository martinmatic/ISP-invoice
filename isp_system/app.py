from flask import Flask, render_template, request, redirect, url_for, flash
import random
import datetime

app = Flask(__name__)
app.secret_key = 'secret'

# Sample Database - Stores customers and invoices
customers = []
invoices = []

class Customer:
    def __init__(self, customer_id, name, email, plan, data_used):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.plan = plan
        self.data_used = data_used

class Invoice:
    def __init__(self, invoice_id, customer_id, amount, due_date):
        self.invoice_id = invoice_id
        self.customer_id = customer_id
        self.amount = amount
        self.due_date = due_date
        self.status = "Unpaid"  # default status

def calculate_invoice(plan, data_used):
    """Calculate the invoice amount based on the plan and data used."""
    base_price = 50  # base price for any plan
    overcharge_rate = 10  # $ per GB over plan limit

    # Assuming different plans have different data limits
    plan_limits = {
        'Basic': 100,  # 100 GB
        'Premium': 300,  # 300 GB
        'Unlimited': float('inf')  # No limit
    }

    data_limit = plan_limits[plan]
    
    if data_used > data_limit:
        extra_data = data_used - data_limit
        return base_price + extra_data * overcharge_rate
    else:
        return base_price

@app.route('/')
def index():
    return render_template('index.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        plan = request.form['plan']
        data_used = request.form['data_used']

        # Create new customer
        customer_id = random.randint(1000, 9999)
        new_customer = Customer(customer_id, name, email, plan, float(data_used))
        customers.append(new_customer)

        flash(f"Customer {name} added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_customer.html')

@app.route('/customers')
def view_customers():
    return render_template('customers.html', customers=customers)

@app.route('/generate_invoice/<int:customer_id>')
def generate_invoice(customer_id):
    # Find customer by ID
    customer = next((cust for cust in customers if cust.customer_id == customer_id), None)
    
    if customer:
        # Calculate the invoice based on plan and data used
        amount_due = calculate_invoice(customer.plan, customer.data_used)
        
        # Generate invoice details
        invoice_id = random.randint(10000, 99999)
        due_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')

        # Create and save invoice
        new_invoice = Invoice(invoice_id, customer_id, amount_due, due_date)
        invoices.append(new_invoice)
        
        flash(f"Invoice generated for {customer.name} - Amount: ${amount_due}", "success")
        return redirect(url_for('view_invoices'))
    else:
        flash("Customer not found!", "danger")
        return redirect(url_for('index'))

@app.route('/invoices')
def view_invoices():
    # List all invoices
    return render_template('invoice.html', invoices=invoices)

if __name__ == '__main__':
    app.run(debug=True)
