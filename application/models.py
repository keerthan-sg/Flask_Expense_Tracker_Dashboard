from application import db
from datetime import datetime

class IncomeExpenses(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(30),nullable=False,default='income')
    category = db.Column(db.String(30),nullable=False,default='rent')
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    amount = db.Column(db.Integer,nullable=False)