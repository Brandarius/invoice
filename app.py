from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
db = SQLAlchemy(app)

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Customer {self.id}: {self.first_name} {self.last_name}>'

# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

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



@app.route('/inventory')
def add_item():
    return render_template('inventory.html')

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    # Assuming you're using SQLAlchemy, you can delete the customer directly from the database
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('list_customers'))

if __name__ == '__main__':
    app.run(debug=True)
