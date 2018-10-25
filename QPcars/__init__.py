import os
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
from QPcars.models import User

db.drop_all()
db.create_all()


@app.route('/app/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.get_json()
        user = User(name=req.get("name"),
                    username=req.get("username"),
                    password=req.get("password"),
                    surName=req.get("surName"),
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


@app.route('/web')
def web():
    return render_template('Hp.html', error=None)


@app.route('/web/login', methods=["POST"])
def login_web():
    un = request.form["username"]
    ps = request.form["password"]
    u = User.get_by_username(un)
    if u is not None and u.check_password(ps):
        login_user(u)
        return redirect(url_for('home'))
    else:
        error = 'Invalid credentials'
        return render_template('Hp.html', error=error)


@app.route('/web/home')
def home():
    return render_template('index.html')
