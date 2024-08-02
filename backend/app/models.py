from app import db
from datetime import datetime, timezone

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    country_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Portfolio(db.Model):
    portfolio_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'id': self.portfolio_id,
            'name': self.name,
            'user_id': self.user_id,
            'date_created': self.date_created
        }
        
    def __repr__(self):
        return f'<Portfolio {self.name}>'
    
class StockHoldings(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, nullable=False)
    ticker = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    fees = db.Column(db.Float)
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<StockHoldings {self.transaction_id}>'
    
class Cash(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    interest = db.Column(db.Float)
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<Cash {self.transaction_id}>'
    
class RealEstate(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    worth = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<RealEstate {self.transaction_id}>'
    
class Debt(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    interest = db.Column(db.Float)
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<Debt {self.transaction_id}>'