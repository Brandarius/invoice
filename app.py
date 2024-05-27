from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_BINDS'] = {'inventory': 'sqlite:///inventory.db', 'invoice_list': 'sqlite:///invoice_list.db'}
db = SQLAlchemy(app)


class Invoice_List(db.Model):
    __bind_key__ = 'invoice_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        
        items = []
        total_amount = 0
        
        for i in range(8):
            item_name = request.form.get(f'item_{i}')
            
            amount_str = request.form.get(f'amount_{i}')
            amount = float(amount_str) if amount_str.strip() else None
            
            quantity_str = request.form.get(f'quantity_{i}')
            quantity = int(quantity_str) if quantity_str.strip() else None
            
            if amount is not None and quantity is not None:
                price = amount * quantity
                total_amount += price
            else:
                price = None
                
            items.append({
                'item_name': item_name,
                'amount': amount,
                'quantity': quantity,
                'price': price
            })
        new_invoice = Invoice_List(name=name, amount=total_amount, date=date)
        db.session.add(new_invoice)
        db.session.commit()
        
        return redirect(url_for('invoice_list'))
    
    items = [{'item_name': '', 'amount': '', 'quantity': '', 'price': ''} for _ in range(8)]
    return render_template('main_page.html', items=items, total_amount=0)




@app.route('/invoice_list')
def invoice_list():
    invoices = Invoice_List.query.all()
    return render_template('invoice_list.html', invoices=invoices)


if __name__ == '__main__':
    app.run(debug=True)



Isaac = 'YourMom'