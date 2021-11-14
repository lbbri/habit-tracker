from app import app, bp, db
from models import UserCredential, Habit
from database import getUserHabits, addUserHabit
import os
import json
import requests
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
import base64


@bp.route('/index')
# @login_required
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {"habits": getUserHabits()}
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )

@bp.route('/create', methods=["POST"])
def createHabit():
    response_json = flask.request.json
    addUserHabit(response_json)

    return flask.jsonify({"status":'success'}) #TODO: update to something more meaningful

app.register_blueprint(bp)


@app.route('/signup')
def signup():
    return flask.render_template("sign-up.html")


@app.route('/signup', methods=["POST"])
def signup_post():
    signup_username = flask.request.form.get('username')
    signup_email = flask.request.form.get('email')
    signup_password = flask.request.form.get('password')
    signup_password_confirm = flask.request.form.get('confirmpassword')

    input_signup_email = UserCredential.query.filter_by(
        email=signup_email).first()

    # Check if email already in database
    if input_signup_email:
        flask.flash("This email has already been used. Try something else!")
        return flask.redirect(flask.url_for("signup"))

    # Check if password and confirm does not matched
    if signup_password_confirm != signup_password:
        flask.flash("Your Password did not match. Try again!")
        return flask.redirect(flask.url_for("signup"))

    # Pass all conditions, add info to database with encrypted password
    else:
        encrypt_signup_password = base64.b64encode(
            signup_password.encode("utf-8"))
        signupuser = UserCredential(username=signup_username, email=signup_email,
                                    password=str(encrypt_signup_password))
        db.session.add(signupuser)
        db.session.commit()
        # login_user(signupuser)
        return flask.redirect(flask.url_for("bp.index"))


@app.route('/login')
def login():
    return flask.render_template("log-in.html")


@app.route('/login', methods=["POST"])
def login_post():
    login_email = flask.request.form.get('email')
    login_password = flask.request.form.get('password')
    encrypt_login_password = base64.b64encode(
        login_password.encode("utf-8"))

    login_user = UserCredential.query.filter_by(
        email=login_email, password=str(encrypt_login_password)).first()

    # Check if email and password match with database
    if not login_user:
        flask.flash("Invalid email or password. Try again!")
        return flask.redirect(flask.url_for("login"))

    # Redirect user into main page if email and password matched
    else:
        # login_user(login_user)
        return flask.redirect(flask.url_for("bp.index"))


@app.route('/')
def main():
    #return flask.redirect(flask.url_for('login'))
    return flask.redirect(flask.url_for("bp.index"))



if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8081)),
        debug=True,
    )