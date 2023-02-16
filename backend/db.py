from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class cb_list(db.Model):
    __tablename__ = 'cb_list'
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    expire = db.Column(db.String(20))

    def __init__(self, code, name, expire):
        self.code = code
        self.name = name
        self.expire = expire

    def __repr__(self):
        return '<cb_list %r>' % self.name

class jsy_data(db.Model):
    __tablename__ = 'jsy_data'
    code = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    date = db.Column(db.Date, primary_key=True)

    def __init__(self, code, price, date):
        self.code = code
        self.price = price
        self.date = date

    def __repr__(self):
        return '<jsy_data %r %r>' % (self.code, self.date)

class inc_data(db.Model):
    __tablename__ = 'inc_data'
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    inc_d = db.Column(db.String(10))
    inc_w = db.Column(db.String(10))
    inc_m = db.Column(db.String(10))
    expire = db.Column(db.String(20))

    def __init__(self, code, name, inc_d, inc_w, inc_m, expire):
        self.code = code
        self.name = name
        self.inc_d = inc_d
        self.inc_w = inc_w
        self.inc_m = inc_m
        self.expire = expire

    def __repr__(self):
        return '<inc_data %r %r>' % (self.code, self.name)

class follow(db.Model):
    __tablename__ = 'follow'
    code = db.Column(db.Integer, primary_key=True)
    add_date = db.Column(db.Date)

    def __init__(self, code):
        self.code = code
        self.add_date = date.today()

    def __repr__(self):
        return '<follow %r>' % self.code