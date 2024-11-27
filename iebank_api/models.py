from iebank_api import db
from datetime import datetime
import string, random

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default = 0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Event %r>' % self.account_number

    def __init__(self, name, user_id, currency):
        self.name = name
        self.user_id = user_id
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.balance = 100
        self.status = "Active"



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.username

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_from = db.Column(db.Integer, nullable=False)
    user_to = db.Column(db.Integer, nullable=False)
    account_from = db.Column(db.Integer, nullable=False)
    account_to = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.id

    def __init__(self, user_from, user_to, account_from, account_to, amount):
        self.user_from = user_from
        self.user_to = user_to
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount