from app import app, bp, db
from models import Usercredential, Habit
import os
import json
import requests
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from datetime import date
import base64


@bp.route('/index')
# @login_required
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {"your": "data here"}
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )


@bp.route('/save', methods=["POST"])
def saveTestHabit():
    response_json = flask.request.json
    print(response_json)
    title = response_json['title']
    category = response_json['category']
    date_created = date.today()
    target_days = response_json['target_days']

    # habit = Habit(
    #     user=10,  # hardcoded user id for test purposes
    #     title=response_json['title'],
    #     category=response_json['category'],
    #     date_created=date.today(),
    #     target_days=response_json['target_days'],
    # )

    db.session.add(habit)
    db.session.commit()

    # change this to something more meaningful
    return flask.jsonify({"status": 'success'})


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

    # All fields must be input
    if not signup_username or not signup_email or not signup_password or not signup_password_confirm:
        flask.flash("All fields must be input!")
        return flask.redirect(flask.url_for("signup"))

    input_signup_email = Usercredential.query.filter_by(
        email=signup_email).first()

    # Check if email already in database
    if input_signup_email:
        flask.flash("The email has been taken. Try something else!")
        return flask.redirect(flask.url_for("signup"))

    # Check if password and confirm does not matched
    if signup_password_confirm != signup_password:
        flask.flash("Your Password did not match. Try again!")
        return flask.redirect(flask.url_for("signup"))

    # Pass all conditions, add info to database with encrypted password
    else:
        encrypt_signup_password = base64.b64encode(
            signup_password.encode("utf-8"))
        signupuser = Usercredential(username=signup_username, email=signup_email,
                                    password=encrypt_signup_password)
        db.session.add(signupuser)
        db.session.commit()
        # login_user(signupuser)
        return flask.redirect(flask.url_for("bp.index"))


@app.route('/login')
def login():
    return flask.render_template("log-in.html")


@app.route('/login', methods=["POST"])
def login_post():
    ...


@app.route('/')
def main():
    return flask.redirect(flask.url_for('login'))


if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8081)),
        debug=True,
    )
