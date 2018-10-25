import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.login_view = 'login'
# manager = Manager(app)
from QPcars.models import User, Car

db.drop_all()
db.create_all()


@app.route('/app/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.get_json()
        user = User(name=req.get("name"),
                    username=req.get("username"),
                    password=req.get("password"),
                    lastName=req.get("lastName"),
                    age=req.get("age"),
                    id=req.get("id"),
                    address=req.get("address"),
                    gender=req.get("gender"),
                    postalCode=req.get("postalCode"),
                    email=req.get("email"))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        print("signed in")
        return ""


@app.route('/app/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req = request.get_json()
        username = req.get("username")
        password = req.get("password")
        u = User.get_by_username(username=username)
        if u is not None and u.check_password(password):
            login_user(u)
            return jsonify(u.serialize())
        else:
            return "wrong username or password"


@app.route('/app/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/app/listUsers')
def list():
    if request.method == "GET":
        users = User.query.all()
        return jsonify([user.serialize() for user in users])


@app.route('/app/addCar', methods=["POST"])
@login_required
def add_car():
    if request.method == "POST":
        req = request.get_json()
        if User.query.filter_by(id=req.get("user_id")).first() is not None:
            car = Car(name=req.get("name"),
                      factory=req.get("factory"),
                      kilometer=req.get("kilometer"),
                      year=req.get("year"),
                      color=req.get("color"),
                      description=req.get("description"),
                      automate=req.get("automate"),
                      user_id=req.get("user_id"),
                      price=req.get("price"))
            db.session.add(car)
            db.session.commit()
            print("car added")
            return jsonify(car.serialize())


@app.route('/app/listCar', methods=["GET"])
@login_required
def list_car():
    if request.method == "GET":
        cars = Car.query.all()
        return jsonify([car.serialize() for car in cars])


@app.route('/web/login_page')
@login_required
def web_login_page():
    return render_template('Hp.html', error=None)


@app.route('/web/login', methods=["POST"])
def web_login():
    un = request.form["username"]
    ps = request.form["password"]
    u = User.get_by_username(un)
    if u is not None and u.check_password(ps):
        login_user(u)
        return redirect(url_for('home'))
    else:
        error = 'Invalid credentials'
        return render_template('Hp.html', error=error)


@app.route('/web/signup_page')
def web_signup_page():
    return render_template('signup.html', error=None)


@app.route('/web/signup',methods=["POST"])
def web_signup():
    name = request.form["name"]
    lastname = request.form["family"]
    id = request.form["IdNumber"]
    age = request.form["age"]
    mobile_num = request.form["mobileNumber"]
    phone_num = request.form["phoneNumber"]
    username = request.form["username"]
    email = request.form["email"]
    gender = request.form["gender"]
    password = request.form["pass"]
    cpass = request.form["cpass"]
    error = None
    if User.get_by_username(username) is not None or User.get_by_email(email) is not None:
        error = 'Username or email is already taken'
    if password == cpass:
        print("checked")
        u = User(name=name,username=username,
                 lastName=lastname,age=age,
                 identificationId=id,gender=gender,
                 mobile_num=mobile_num,phone_num=phone_num,
                 email=email,password=password)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        print("signed in")
    else:
        error = 'The two passwords are different!'
    if error:
        return render_template('signup.html',error = error)
    return redirect(url_for('home'))


@app.route('/web/home')
def home():
    return render_template('index.html')
