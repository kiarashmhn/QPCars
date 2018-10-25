from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from QPcars import *
from QPcars.forms import *


"""class UserLog:
@app.route('/app/login', methods=["GET", "POST"])
    def login():
        pass

    # app.add_url_rule('/login.html', view_func=Login.login)
    @app.route('/app/logout')
    def logout():
        logout_user()
        return redirect(url_for("signup"))"""


@app.route('/app/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = User(name=request.form["name"],surName=request.form["surName"],age=request.form["age"],id=request.form["id"],address=request.form["address"],gender=request.form["gender"],postalCode=request.form["postalCode"],username=request.form["username"],email=request.form["email"])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        print("signed in")
        return ""


@app.route('/')
def show_all():
    return "HI!"


app.run(debug=True)
