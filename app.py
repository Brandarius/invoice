from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'  # SQLite database
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Add more columns as needed (e.g., address, email, etc.)

    def __repr__(self):
        return '<Customer %r>' % self.name
    '''
@app.route('/')
def main_page():
    return render_template('main_page.html')
'''
@app.route('/customers')
def customers():
    return render_template('customers.html')
'''
if __name__ == '__main__':
    app.run(debug=True)