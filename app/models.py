from app import db
from flask_login import UserMixin

user_stocks = db.Table('user_stocks',
            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
            db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True)
)


class Stock(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ticker = db.Column(db.String(50), nullable=False)
	date = db.Column(db.Date)
	price = db.Column(db.String(50), nullable=False)
    
@staticmethod
def delete_stock(ticker):
        Stock.query.filter_by(ticker=ticker).delete()
        db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    stocks = db.relationship('Stock', secondary=user_stocks, lazy='subquery',
                                       backref=db.backref('app_users', lazy=True))
