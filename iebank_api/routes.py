from flask import Flask, request
from iebank_api import db, app
from iebank_api.models import Account, User, Transaction

from iebank_api import default_username, default_password

from sqlalchemy import or_

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '
    
    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text


@app.route('/accounts', methods=['POST'])
def create_account():
    name = request.json['name']
    user_id = request.json['user_id']
    currency = request.json['currency']
    account = Account(name, user_id, currency)
    db.session.add(account)
    db.session.commit()
    return format_account(account)

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'user_id': account.user_id,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'status': account.status,
        'created_at': account.created_at
    }



@app.route('/admin', methods=['POST'])
def admin_login():
    username = request.json['username']
    password = request.json['password']

    print("ADMIN TRIED LOGGING IN", username, password)
    valid = verify_admin(username, password)
    print("VALID:", valid)
    return {'result': valid}

def verify_admin(username, password):
    print("Given:", username, password, "     real:", default_username, default_password, "     result:", username == default_username and password == default_password)
    return username == default_username and password == default_password




@app.route('/users', methods=['POST'])
def create_user():
    print(request.json)
    username = request.json['username']
    password = request.json['password']
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return format_user(user)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return {'users': [format_user(user) for user in users]}

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return format_user(user)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.username = request.json['username']
    db.session.commit()
    return format_user(user)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return format_user(user)

def format_user(user):
    return {
        'id': user.id,
        'username': user.username,
    }



@app.route('/users/login', methods=['POST'])
def user_login():
    username = request.json['username']
    password = request.json['password']

    print("USER TRIED LOGGING IN", username, password)
    valid, user_id = verify_user(username, password)
    print("VALID:", valid)
    return {'result': valid, 'user_id': user_id}

def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        print("User not found.")
        return False, -1
    else:
        print("User exists. Given password:", password, "     real:", default_password)
        return user.password == password, user.id
    


@app.route('/accounts/users/<int:id>', methods=['GET'])
def get_user_accounts(id):
    accounts = Account.query.filter_by(user_id=id).all()
    return {'accounts': [format_account(account) for account in accounts]}


# request = ['user_from', 'account_from', 'account_to', 'amount']
@app.route('/transactions', methods=['POST'])
def make_transaction():
    print(request.json)
    
    user_from = request.json['user_from']

    account_from = request.json['account_from']
    account_to = request.json['account_to']

    amount = int(request.json['amount'])
    print("TRANSACTION AMOUNT", amount)
    
    db_account_from = Account.query.filter_by(account_number=account_from).first()
    db_account_to = Account.query.filter_by(account_number=account_to).first()

    if not db_account_from or not db_account_to:
        return {"valid" : False, "message" : "Invalid account."}

    if str(db_account_from.user_id) != str(user_from):
        return {"valid" : False, "message" : "Can only make transactions from your accounts."}

    if amount > db_account_from.balance:
        return {"valid" : False, "message" : "Insufficient balance."}
    
    user_to = db_account_to.user_id

    db_account_from.balance -= amount
    db_account_to.balance += amount
    print("NEW BALANCE", db_account_from.balance)

    transaction = Transaction(user_from, user_to, account_from, account_to, amount)
    db.session.add(transaction)
    db.session.commit()
    return {"valid" : True, "message" : "Transaction successful!"}


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return {'transactions': [format_transaction(transaction) for transaction in transactions]}


@app.route('/transactions/<int:id>', methods=['GET'])
def get_user_transactions(id):
    transactions = Transaction.query.filter(or_(Transaction.user_from==id, Transaction.user_to==id)).all()
    return {'transactions': [format_transaction(transaction) for transaction in transactions]}


def format_transaction(transaction):
    return {
        'id': transaction.id,
        'account_from': transaction.account_from,
        'account_to' : transaction.account_to,
        'user_from': transaction.user_from,
        'user_to' : transaction.user_to,
        'amount' : transaction.amount,
    }