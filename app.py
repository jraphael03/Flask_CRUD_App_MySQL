from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   # Telling which module will control the application

# @app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Connect to the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Opendoors744784@localhost/studentdb'  # Username: password @ host/ db name

# create a database table ( connect to the created app )
db = SQLAlchemy(app)
class CheckingAccount( db.Model):       # class will be the name of the db table
    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String(100), nullable=False )
    balance = db.Column( db.Float, nullable=False )
    def __repr__(self):
        return str(self.id) + ", " + str(self.name) + ", " + str(self.balance)

# POST AND GET FROM DATABASE
@app.route('/', methods=['POST', 'GET'])     # http://localhost:5000/       The methods we can use with this route
def index():
    # Inside we need to set up each action
    print("inside index")
    if request.method == 'POST':
        name = request.form['name']     # initialize name and balance then pass
        balance = request.form['balance']
        account = CheckingAccount(name=name, balance=balance)
        try:
            db.session.add(account)     # try to add to db then commit
            db.session.commit()
            return redirect('/')        # Go back to index.html and display using GET under
        except: 
            return "Add error"
    else:   # If it's not a POST it is a GET
        accounts = CheckingAccount.query.order_by(CheckingAccount.id).all()     # Same as SELECT * FROM Checking_Account ORDER BY Id
        return render_template('index.html', accounts = accounts)        # render the template we created, passing in accounts varibale array as accounts


# DELETE DATA FROM THE DATABASE
@app.route('/delete/<int:id>')     # http://localhost:5000/delete/id       The methods we can use with this route
def delete( id):
    print("inside delete")
    account = CheckingAccount.query.get_or_404(id)
    try:
        db.session.delete(account)     # try to add to db then commit
        db.session.commit()
        return redirect('/')        # Go back to index.html and display using GET under
    except: 
        return "Delete error"


# UPDATE DATA IN THE DATABASE
@app.route('/update/<int:id>', methods=['POST', 'GET'])     # http://localhost:5000/       The methods we can use with this route
def update( id):
    # Inside we need to set up each action
    print("inside update")
    account = CheckingAccount.query.get_or_404(id)  # SELECT * FROM CHECKING_ACCOUNT WHERE Id = id
    if request.method == 'POST':
        account.name = request.form['name']     # initialize name and balance then pass
        account.balance = request.form['balance']
        try:
            db.session.commit()
            return redirect('/')        # Go back to index.html and display using GET under
        except: 
            return "Update error"
    else:   # If it's not a POST it is a GET
        return render_template('update.html', account = account)        # render the template we created, passing in account varibale array as account


if __name__ == '__main__':
    app.run(debug=True, host='localhost')