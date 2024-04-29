from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'  # SQLite database
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email_address = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    

    def __repr__(self):
        return '<Customer %r>' % self.name

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
        new_name = request.form['new_name']
        if new_name:
            customer.name = new_name
            db.session.commit()
    return redirect(url_for('customers'))


if __name__ == '__main__':
    app.run(debug=True)