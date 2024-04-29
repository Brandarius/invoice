from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email_address = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<Customer %r>' % self.id

# Create the database tables
with app.app_context():
    db.create_all()
    
    
    
    
@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html',customers=customers)

@app.route('/update/<int:id>', methods=['POST'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        new_first_name = request.form['new_first_name']
        new_last_name = request.form['new_last_name']
        new_email_address = request.form['new_email_address']
        new_address = request.form['new_address']
        new_phone_number = request.form['new_phone_number']

        # Update only if the field is not empty
        if new_first_name:
            customer.first_name = new_first_name
        if new_last_name:
            customer.last_name = new_last_name
        if new_email_address:
            customer.email_address = new_email_address
        if new_address:
            customer.address = new_address
        if new_phone_number:
            customer.phone_number = new_phone_number

        db.session.commit()
    return redirect(url_for('customers'))


if __name__ == '__main__':
    app.run(debug=True)