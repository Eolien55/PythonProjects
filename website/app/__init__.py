import hashlib
import datetime
from numpy import random
from urllib.parse import unquote
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import os
import subprocess
import re

__version__ = "1.0.0"
import flask

app = flask.Flask(__name__)

password = "052cf1ebd71d676a64f2e4a8926155702996989cba7a974133a88ec996878960db0c782643e25c3465db0fcc329417bc5ae4eb99a14b8606d63018aae9cbe05b"
app.secret_key = "oof"
UPLOAD_FOLDER = "/home/elie/Documents/usb"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.before_request
def sessionlive():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)


############################################ USB A DISTANCE ############################################


@app.route("/files/path/<path:file>", methods=["GET"])
def menu(file="/"):
    file = "/" + file
    isallowed = False
    if "allowed/" in file and file.index("allowed/") < 2:
        file = file.replace("allowed/", "/home/elie/Documents/")
        isallowed = True
    else:
        if "username" not in flask.session:
            return flask.redirect("/files/login")
        elif (
            not hashlib.sha512(bytes(flask.session["username"], "UTF-8")).hexdigest()
            == password
        ):
            return flask.redirect("/files/login")
    if "allowed/" in file and file.index("allowed/") < 2:
        file.replace("allowed/", "/home/elie/Documents/")
    if not os.path.exists(file):
        file = file.replace("+", " ")
    if not os.path.exists(file):
        file = unquote(file)
    if not os.path.exists(file):
        return (
            open(
                "/home/elie/pythonprojects/website/app/usbadistance/404.html", "r"
            ).read(),
            404,
        )
    if os.path.isdir(file):
        try:
            previous = file[::-1][file[::-1].index("/") + 1 :][::-1]
        except ValueError:
            return (
                open(
                    "/home/elie/pythonprojects/website/app/usbadistance/404.html",
                    "r",
                ).read(),
                404,
            )
        file2 = open(
            "/home/elie/pythonprojects/website/app/usbadistance/a.html", "r"
        ).read()
        temp = """%s"""
        for cd, subs, files in os.walk(file):
            if cd != file:
                break
            for i in subs:
                temp = (
                    temp
                    % (
                        (
                            """<a href="/files/path/%s" style="color: #FFFFFF; font-size:25px"><div class="file">\n<p style="margin-left:50px;" class="%s"> %s </p></div></a>"""
                            % (
                                file + "/" + i.replace(" ", "+")
                                if not isallowed
                                else "allowed"
                                + "/"
                                + file[
                                    file.index("/home/elie/Documents/")
                                    + len("/home/elie/Documents/") :
                                ]
                                + "/"
                                + i.replace(" ", "+"),
                                "%s",
                                i,
                            )
                        )
                    )
                    % ("folder" if os.path.isdir(file + "/" + i) else "afile")
                    + "%s"
                )
            for i in files:
                temp = (
                    temp
                    % (
                        (
                            """<a href="/files/path/%s" style="color: #FFFFFF; font-size:25px">\n<div class="file">\n<p style="margin-left:50px;" class="%s"> %s </p>\n</div>\n</a>\n"""
                            % (
                                file + "/" + i.replace(" ", "+")
                                if not isallowed
                                else "allowed"
                                + "/"
                                + file[
                                    file.index("/home/elie/Documents/")
                                    + len("/home/elie/Documents/") :
                                ]
                                + "/"
                                + i.replace(" ", "+"),
                                "%s",
                                i,
                            )
                        )
                    )
                    % ("folder" if os.path.isdir(file + "/" + i) else "afile")
                    + "%s"
                )
        temp = "".join(temp)
        temp = temp.replace("%s", "")
        file2 = file2 % (
            ("/files/add/%s" % file),
            "/files/path/" + previous.replace(" ", "+")
            if not isallowed
            else "files/path/allowed"
            + "/"
            + file[
                file.index("/home/elie/Documents/") + len("/home/elie/Documents/") :
            ][::-1][file[::-1].index("/") + 1 :][::-1],
            temp,
        )
        return file2
    else:
        try:
            return flask.send_file(file)
        except FileNotFoundError:
            return flask.send_file(file.replace("+", " "))


def allowed_file(filename):
    return bool(filename)


@app.route("/files/add/", methods=["GET"])
def redir():
    return flask.redirect("/files/add//home")


@app.route("/files/add/<path:prevfile>", methods=["GET", "POST"])
def imma_upload_ur_mother(prevfile):
    prevfile = "/" + prevfile
    if "username" not in flask.session:
        return flask.redirect("/files/login")
    elif (
        not hashlib.sha512(bytes(flask.session["username"], "UTF-8")).hexdigest()
        == password
    ):
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return flask.redirect(f"/files/path/{prevfile}")
    return open(
        "/home/elie/pythonprojects/website/app/usbadistance/add.html", "r"
    ).read() % ("files/path/" + prevfile,)


@app.route("/files/")
def welcome():
    return open(
        "/home/elie/pythonprojects/website/app/usbadistance/welcome.html", "r"
    ).read()


@app.route("/files/login/", methods=["GET", "POST"])
def login():
    if "tries" in flask.session:
        if flask.session["tries"] == 4:
            return (
                """
            <html>
            <head>
            <title>Trop d'erreurs</title>
            <link rel="preconnect" href="https://fonts.gstatic.com">
            <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
            <style>
            body {
                font-size:60px;
                color:#009cd1;
                font-family: 'Roboto', sans-serif;
                background: url('/images/backgroundn0.jpg');
                background-size:  cover;
            }
            h1 {
                position:relative;
                text-align:center;
                margin-top:100px;
                margin-bottom:100px;
            }
            </style>
            </head>
            <body>
            <h1>
            Trop d'erreurs, par s&eacute;curit&eacute;, tu ne passes pas.
            </html>""",
                403,
            )  # Page d'erreur
    if flask.request.method == "GET":
        return """
        <html>
        <head>
        <title>login</title>
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <style>
        body {
                color:white;
                font-family: 'Roboto', sans-serif;
                background: url('/images/backgroundn0.jpg');
                background-size:  cover;
            }
        input {
            border: none;
            background:transparent;
            color:#009cd1;
            font-size: 50px;
        }
        form {
            position:relative;
            margin-left:300px;
            margin-top:300px;
            margin-right:300px;
            margin-bottom:300px;
        }
        </style>
        </head>
        <body>
        <form action = "" method = "post">
      <input type = "password" name = username style="background-color:white;">
      <input type = submit value = Login>
   </form>
   </body>
   </html>
   """
    if (
        hashlib.sha512(bytes(flask.request.form["username"], "UTF-8")).hexdigest()
        == password
    ):
        flask.session["username"] = flask.request.form["username"]
        return flask.redirect("/files")
    else:
        try:
            flask.session["tries"] += 1
        except KeyError:
            flask.session["tries"] = 0
        return """<body style="color:white;font-family:sans-serif;background: url('/images/backgroundn0.jpg');background-size:  cover;">invalid password</body>"""


@app.route("/files/logout")
def logout():
    try:
        flask.session.pop("username", None)
    except Exception as e:
        print(e)
    return ""


@app.route("/images/<path:string>")
def imgfile(string):
    try:
        return flask.send_file(
            r"/home/elie/pythonprojects/website/app/templates/usb/" + string
        )
    except FileNotFoundError:
        return ""


############################################ USB A DISTANCE ############################################
############################################ PAGE "A PROPOS" ############################################
@app.route("/about/")
def about():
    projects = eval(
        open(
            "/home/elie/pythonprojects/website/app/templates/about/database", "r"
        ).read()
    )
    return flask.render_template_string(
        open(
            "/home/elie/pythonprojects/website/app/templates/about/about.html", "r"
        ).read(),
        projects=projects,
        cont=0,
    )


@app.route("/about/<int:pk>/")
def project(pk):
    thisproject = eval(
        open(
            "/home/elie/pythonprojects/website/app/templates/about/database", "r"
        ).read()
    )[1][pk - 1]
    if isinstance(thisproject["longdescription"], list):
        projects = eval(
            open(
                "/home/elie/pythonprojects/website/app/templates/about/database", "r"
            ).read()
        )
        return flask.render_template_string(
            open(
                "/home/elie/pythonprojects/website/app/templates/about/about.html",
                "r",
            ).read(),
            projects=projects,
            cont=thisproject["longdescription"][0],
        )
    return flask.render_template_string(
        open(
            "/home/elie/pythonprojects/website/app/templates/about/projects.html",
            "r",
        ).read(),
        project=thisproject,
        title=thisproject["title"],
    )


############################################ PAGE "A PROPOS" ############################################
############################################ PAGE DE BASE ############################################
@app.route("/")
def welcomehere():
    background = "background%s.jpg" % random.choice(
        range(
            len(
                [
                    i
                    for i in os.listdir(
                        r"/home/elie/pythonprojects/website/app/templates/usb/"
                    )
                    if i.startswith("background") and i.endswith(".jpg")
                ]
            )
        )
    )
    return flask.render_template_string(
        open("/home/elie/pythonprojects/website/app/welcome.html", "r").read(),
        background=background,
    )


@app.route("/todo/")
def todo():
    file = open("/home/elie/desktop/scripts/todo.txt", "r").read()
    file = file.split("\\")
    return flask.render_template_string(
        open("/home/elie/pythonprojects/website/app/todo.html", "r").read(),
        file=file,
    )


"""@app.route("/cmd/", methods=["GET", "POST"])
def cmd():
    if "username" not in flask.session:
        return flask.redirect("/files/login")
    elif (
        not hashlib.sha512(
            bytes(flask.session["username"], "UTF-8")).hexdigest()
        == password
    ):
        return flask.redirect("/files/login")
    if flask.request.method == "POST":
        if 1:
            za_command = unquote(flask.request.form["command"])
            stdin = flask.request.form["stdin"]
            stdin = stdin.split('\n')
            open('/home/elie/pythonprojects/website/app/.sh', 'w').write(za_command)
            os.system("chmod +x /home/elie/pythonprojects/website/app/.sh")
            process = subprocess.Popen(
                '/home/elie/pythonprojects/website/app/.sh', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text="UTF-8")
            print(stdin, za_command)
            for line in stdin:
                process.stdin.write(line+'\n')
            \"""while 1:
                break
                if process.poll() is not None:
                    break\"""
            with process.stdout:
                return flask.jsonify({"result": re.sub(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]',
                                                       '', process.stdout.read(), flags=re.IGNORECASE)})
    return open("/home/elie/pythonprojects/website/app/cmd.html", "r").read()"""


############################################ PAGE DE BASE ############################################
############################################ ERREURS ############################################


@app.errorhandler(HTTPException)
def error(err):
    err = err.code
    errors = {
        404: "Cette URL n'existe pas",
        500: "Erreur interne (erreur dans le code ou impossible d'acc&eacute;der &agrave; ce fichier)",
    }
    return flask.render_template_string(
        open("/home/elie/pythonprojects/website/app/error.html", "r").read(),
        erreur=err,
        message=errors[err],
    )
