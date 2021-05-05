import flask
import hashlib
from website.url import app, db


class url(db.Model):
    id = db.Column(db.String(7), primary_key=True)
    real_url = db.Column(db.String(), index=True, unique=True)


@app.route("/", methods=["GET", "POST"])
def welcome():
    if flask.request.method == "POST":
        shortened = flask.request.form["url"]
        while True:
            try:
                shortened = hashlib.sha3_512(bytes(shortened, "UTF-8")).hexdigest()
                new = url(
                    id=shortened[:7],
                    real_url=flask.request.form["url"],
                )
                db.session.add(new)
                db.session.commit()
                return new.id
            except:
                pass
    return open("home.html", "r").read()


@app.route("/<string:realurl>")
def redirect(realurl):
    return flask.redirect(url.query.get(realurl).real_url)


@app.route("/img/<path:file>")
def returnfile(file):
    try:
        return flask.send_file(
            r"C:\Users\elie\PythonProjects\website\app/templates\usb/" + file
        )
    except FileNotFoundError:
        return ""
