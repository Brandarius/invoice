from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_BINDS'] = {'inventory': 'sqlite:///inventory.db'}
db = SQLAlchemy(app)

#Database Creation and Bull Crap 
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f'<Customer {self.id}: {self.first_name} {self.last_name}>'

# Inventory model
class InventoryItem(db.Model):
    __bind_key__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Database creation
with app.app_context():
    db.create_all()

@app.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

# Function to Add Customers
@app.route('/add_customer', methods=['POST'])
def add_customer():
    new_customer = Customer(
        first_name=request.form['new_firstname'],
        last_name=request.form['new_lastname'],
        email_address=request.form['new_email_address'],
        address=request.form['new_address'],
        phone_number=request.form['new_phonenumber']
    )
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('list_customers'))

#Function to delete Customers(Still need to add confirmation window)
@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('list_customers'))

#Search for customers
@app.route('/search_customers')
def search_customers():
    search_lastname = request.args.get('search_lastname', '')
    customers = Customer.query.filter_by(last_name=search_lastname).all()
    return render_template('customers.html', customers=customers)


#The Main Page with the invoice creation that hasnt been set up yet
@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        # Handle form submission here
        copy_firstname = request.form['copy_firstname']
        copy_lastname = request.form['copy_lastname']
        copy_email_address = request.form['copy_email_address']
        copy_address = request.form['copy_address']
        copy_phone_number = request.form['copy_phone_number']
        
        return render_template('main_page.html', 
                               copy_firstname=copy_firstname,
                               copy_lastname=copy_lastname,
                               copy_email_address=copy_email_address,
                               copy_address=copy_address,
                               copy_phone_number=copy_phone_number)
    else:
            return render_template('main_page.html')

#Inventory page without the add item function yet
@app.route('/inventory')
def inventory_list():
    inventory_items = InventoryItem.query.all()
    return render_template('inventory.html', inventory_items=inventory_items)

# Route to add item to inventory
@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        new_item = InventoryItem(
            name=request.form['item_name'],
            quantity=int(request.form['item_quantity'])
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('inventory_list'))
    else:
        # Handle other HTTP methods (e.g., GET) if needed
        return "Method Not Allowed", 405
    
@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if request.method == 'POST':
        inventory_item = InventoryItem.query.get_or_404(item_id)
        db.session.delete(inventory_item)
        db.session.commit()
        return redirect(url_for('inventory_list'))
    else:
        return "Method Not Allowed", 405

if __name__ == '__main__':
    app.run(debug=True)
