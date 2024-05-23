from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_BINDS'] = {'inventory': 'sqlite:///inventory.db', 'invoice_list': 'sqlite:///invoice_list.db'}
db = SQLAlchemy(app)


class Invoice_List(db.Model):
    __bind_key__ = 'invoice_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

# Database creation
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        address = request.form['address']
        new_invoice = Invoice_List(name=name, amount=amount)
        db.session.add(new_invoice)
        db.session.commit()
 
    return render_template('main_page.html')

@app.route('/invoice_list')
def invoice_list():
    invoices = Invoice_List.query.all()
    return render_template('invoice_list.html', invoices=invoices)


if __name__ == '__main__':
    app.run(debug=True)



Isaac = 'YourMom'