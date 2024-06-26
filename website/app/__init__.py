import hashlib
import datetime
from urllib.parse import unquote
from werkzeug.exceptions import HTTPException
import os
import time

__version__ = "1.0.0"
import flask

app = flask.Flask(__name__)

iplist = {"timestamp": time.time()}

password = [
    "052cf1ebd71d676a64f2e4a8926155702996989cba7a974133a88ec996878960db0c782643e25c3465db0fcc329417bc5ae4eb99a14b8606d63018aae9cbe05b",
    "3cca0e5d48a670fd48bfc64d337df4bde11122eab1fdf7d1078525acea5ee046ee74bdb9ba14abc41e05c0d2bcea047d898d6167886c5ec5b176d9d70e2d8436",
]

app.secret_key = "oof"
UPLOAD_FOLDER = "/home/eolien55/Documents/usb"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.before_request
def sessionlive():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)


############################################ LOGIN ############################################


def login():
    global iplist
    print(iplist)
    ip = flask.request.environ.get("HTTP_X_FORWARDED_FOR")
    if not ip:
        ip = flask.request.environ.get("REMOTE_ADDR")
        if not ip:
            return 0
    if time.time() - iplist["timestamp"] >= 300:
        iplist = {"timestamp": time.time()}
        return False
    if ip not in iplist:
        return False
    if id_password := flask.session.get("password"):
        return hashlib.sha512(bytes(id_password, "UTF-8")).hexdigest() in password
    return False


############################################ USB A DISTANCE ############################################


@app.route("/files/path/", methods=["GET"])
@app.route("/files/path/<path:path>", methods=["GET"])
def files(path="/"):
    if not path.startswith("allowed"):
        allowed = False
        path = "/" + path
        if not login():
            return flask.redirect("/files/login")
    else:
        allowed = True
        path = path.replace("allowed", "/home/eolien55/Documents")
    if not os.path.exists(path):
        path = unquote(path)
    if not os.path.exists(path):
        path = path + ".html"
    if not os.path.exists(path):
        flask.abort(404)
    if not os.path.isdir(path):
        return flask.send_file(path)
    parent = os.path.abspath(os.path.join(path, ".."))
    if not "/home/eolien55/Documents" in parent and allowed:
        parent = path
    things = sorted(os.listdir(path))
    files = [i for i in things if not os.path.isdir(path + "/" + i)]
    folders = [i for i in things if os.path.isdir(path + "/" + i)]
    if allowed:
        path = path.replace("/home/eolien55/Documents", "allowed")
        parent = parent.replace("/home/eolien55/Documents", "allowed")
    with open("/home/eolien55/pythonprojects/website/app/usbadistance/a.html", "r") as file:
        return flask.render_template_string(
            file.read(), parent=parent, files=files, folders=folders, path=path
        )


def allowed_file(filename):
    return bool(filename)


@app.route("/files/add/", methods=["GET", "POST"])
@app.route("/files/add/<path:prevfile>", methods=["GET", "POST"])
def imma_upload_ur_mother(prevfile=""):
    prevfile = "/" + prevfile
    if not login():
        return flask.redirect("/files/login")
    if not prevfile:
        prevfile = "/home"
    if flask.request.method == "POST":
        # check if the post request has the file part
        if "file" not in flask.request.files:
            flask.flash("No file part")
            return flask.redirect(flask.request.url)
        file = flask.request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return flask.redirect(flask.request.url)
        if file and "allowed_file(file.filename)":
            filename = file.filename  # secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return flask.redirect(f"/files/path/{prevfile}")
    return open(
        "/home/eolien55/pythonprojects/website/app/usbadistance/add.html", "r"
    ).read() % ("files/path/" + prevfile,)


@app.route("/files/")
def welcome():
    return open(
        "/home/eolien55/pythonprojects/website/app/usbadistance/welcome.html", "r"
    ).read()


@app.route("/files/login/", methods=["GET", "POST"])
def log_in():
    global iplist
    ip = flask.request.environ.get("HTTP_X_FORWARDED_FOR")
    if not ip:
        ip = flask.request.environ.get("REMOTE_ADDR")
        if not ip:
            flask.abort(501)
    if not ip in iplist:
        iplist.update({ip: 0})
    if iplist[ip] >= 4:
        file = open(
            "/home/eolien55/pythonprojects/website/app/usbadistance/too_much_tries.html",
            "r",
        )
        file_con = file.read()
        file.close()
        return file_con  # Page d'erreur
    if flask.request.method == "GET":
        file = open(
            "/home/eolien55/pythonprojects/website/app/usbadistance/login.html", "r"
        )
        file_con = file.read()
        file.close()
        return file_con
    if (
        hashlib.sha512(bytes(flask.request.form["username"], "UTF-8")).hexdigest()
        in password
    ):
        flask.session["password"] = flask.request.form["username"]
        return flask.redirect("/files")
    else:
        iplist[ip] += 1
        return """<body style="color:white;font-family:sans-serif;background: url('/images/backgroundn0.jpg');background-size:  cover;">invalid password</body>"""


@app.route("/files/logout")
def logout():
    global iplist
    flask.session["password"] = ""
    return flask.redirect("/files/")


@app.route("/images/<path:string>")
def imgfile(string):
    try:
        return flask.send_file(
            r"/home/eolien55/pythonprojects/website/app/templates/usb/" + string
        )
    except FileNotFoundError:
        return ""


############################################ USB A DISTANCE ############################################
############################################ PAGE "A PROPOS" ############################################
@app.route("/about/")
def about():
    projects = eval(
        open(
            "/home/eolien55/pythonprojects/website/app/templates/about/database.json", "r"
        ).read()
    )
    return flask.render_template_string(
        open(
            "/home/eolien55/pythonprojects/website/app/templates/about/about.html", "r"
        ).read(),
        projects=projects,
        cont=0,
    )


@app.route("/about/<int:pk>/")
def project(pk):
    thisproject = eval(
        open(
            "/home/eolien55/pythonprojects/website/app/templates/about/database.json", "r"
        ).read()
    )[1][pk - 1]
    if isinstance(thisproject["longdescription"], list):
        projects = eval(
            open(
                "/home/eolien55/pythonprojects/website/app/templates/about/database.json",
                "r",
            ).read()
        )
        return flask.render_template_string(
            open(
                "/home/eolien55/pythonprojects/website/app/templates/about/about.html",
                "r",
            ).read(),
            projects=projects,
            cont=thisproject["longdescription"][0],
        )
    return flask.render_template_string(
        open(
            "/home/eolien55/pythonprojects/website/app/templates/about/projects.html",
            "r",
        ).read(),
        project=thisproject,
        title=thisproject["title"],
    )


############################################ PAGE "A PROPOS" ############################################
############################################ PAGE DE BASE ############################################
@app.route("/")
def welcomehere():
    with open("/home/eolien55/pythonprojects/website/app/welcome.html", "r") as file:
        return flask.render_template_string(
            file.read(),
            background="#181a1b",
        )


############################################ PAGE DE BASE ############################################
############################################ ERREURS ############################################


@app.errorhandler(HTTPException)
def error(err):
    err = err.code
    with open("/home/eolien55/pythonprojects/website/app/errors.json", "r") as file:
        errors = flask.json.loads(file.read())
    with open("/home/eolien55/pythonprojects/website/app/error.html", "r") as file:
        return (
            flask.render_template_string(
                file.read(),
                erreur=err,
                message=errors[str(err)][1],
                short=errors[str(err)][0],
            ),
            err,
        )
