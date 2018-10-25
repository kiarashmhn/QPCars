from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from QPcars import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    username = db.Column(db.String(80))
    lastName = db.Column(db.String(20), unique=False)
    age = db.Column(db.Integer)
    identificationId = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(20))
    postalCode = db.Column(db.String(21))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String)
    authenticated = db.Column(db.Boolean)
    mobile_num = db.Column(db.String(15))
    phone_num = db.Column(db.String(15))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email = email).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def serialize(self):
        return {
            'name' : self.name,
            'password' : self.password_hash,
            'lastName' : self.lastName,
            'age' : self.age,
            'identificationId' : self.identificationId,
            'address' : self.address,
            'gender' : self.gender,
            'postalCode' : self.postalCode,
            'username' : self.username,
            'email' : self.email,
            'mobile_num': self.mobile_num,
            'phone_num': self.mobile_num
        }


class Car:
    id = db.Column(db.Integer)
    name = db.Column(db.String(20))
    factory = db.Column(db.String(20))
    kilometer = db.Column(db.Integer)
    year = db.Column(db.Integer)
    color = db.Column(db.String(20))
    description = db.Column(db.String(100))
    automate = db.Column(db.Boolean)
    owner = db.Column(db.String(20))
    price = db.Column(db.Integer)

    def __repr__(self):
        return "<Car '{}'>".format(self.username)


