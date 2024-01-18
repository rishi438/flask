from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    user_id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    name=db.Column(db.String(20),unique=True,nullable=False)
    email= db.Column(db.String(120),nullable=False)
    phone_number=db.Column(db.Integer,nullable=False)
    created_on=db.Column(db.DateTime, default=datetime.utcnow)
    balance=db.Column(db.Float,default=0)
    
    def __repr__(self):
        return f"User{self.name},{self.email}"


class Expense(db.Model):
    expense_id = db.Column(db.String(36), primary_key=True,default=lambda:str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    payer_id = db.Column(db.String(36), db.ForeignKey("user.user_id"), nullable=False)
    expense_type = db.Column(db.String(10), nullable=False)
    created_on = db.Column(db.DateTime,  default=datetime.utcnow)
    payer = db.relationship("User", foreign_keys=[payer_id])

    def __repr__(self):
        return f"Expense({self.amount}, {self.payer}, {self.expense_type})"


class Balance(db.Model):
    balance_id = db.Column(db.String(36), primary_key=True,default=lambda:str(uuid.uuid4()))
    creditor_id = db.Column(db.String(36), db.ForeignKey("user.user_id"), nullable=False)
    debitor_id = db.Column(db.String(36), db.ForeignKey("user.user_id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    creditor = db.relationship("User", foreign_keys=[creditor_id])
    debitor = db.relationship("User", foreign_keys=[debitor_id])

    def __repr__(self):
        return f"Balance({self.creditor}, {self.debitor}, {self.amount})"