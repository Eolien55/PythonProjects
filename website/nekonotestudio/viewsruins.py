from website.nekonotestudio import app, db
import datetime
import werkzeug.security
import flask
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


appruins = app


def login(func):
    def wrapper(*args, **kwargs):
        userid = flask.session.get("username")
        password = flask.session.get("password")
        if userid and (user := User.query.get(userid)):
            if user:
                if user.chek_password(password):
                    return func(*args, **kwargs)
        return flask.redirect(flask.url_for("loginhere"))

    return wrapper


class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
    content = db.Column(db.String(), index=True)
    name = db.Column(db.String(), index=True)
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    comments = db.relationship("Comments", backref="post", lazy="dynamic")


class Comments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
    content = db.Column(db.String(), index=True)
    name = db.Column(db.String(), index=True)
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    commented = db.Column(db.Integer(), db.ForeignKey("posts.id"))


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), index=True)
    email = db.Column(db.String(), index=True)
    password_hash = db.Column(db.String(), index=True)
    posts = db.relationship("Posts", backref="author", lazy="dynamic")
    admin = db.Column(db.Integer(), index=True)
    comments = db.relationship("Comments", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = werkzeug.security.generate_password_hash(password)

    def chek_password(self, password):
        return werkzeug.security.check_password_hash(self.password_hash, password)


@appruins.route("/")
def welcome():
    flask.render_template("welcome.html")  # TODO welcome.html


@appruins.route("/posts/<string:name>/<int:id>")
def render_post(name, id):
    post = Posts.query.get(id)
    return flask.jsonify(
        {
            "time": post.time,
            "content": post.content,
            "name": post.name,
            "author": post.author_id,
        }
    )


@appruins.route("/login/", methods=["POST", "GET"])
def loginhere():
    if flask.request.method == "POST":
        username = flask.request.form.get("email")
        password = flask.request.form.get("password")
        if username:
            if password:
                if (user := User.query.filter_by(email=username).first()) is not None:
                    if user.chek_password(password):
                        flask.session.update(
                            {"username": user.id, "password": password}
                        )
                        return flask.redirect("/ok")
                    else:
                        return "ERR"
                else:
                    return "ERR"
            else:
                return "ERR"
        else:
            return "ERR"
    return flask.render_template("login.html", title="Login")


@appruins.route("/signin/")
def signin():
    pass


@appruins.route("/ok")
@login
def ok():
    return "HEEEEY"
