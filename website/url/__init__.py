__version__ = "1.0.0"

import os
import sys

try:
    os.chdir("url")
except:
    pass
sys.path.append(os.path.abspath(os.path.curdir))
import flask
import flask_sqlalchemy
from flask_migrate import Migrate
from website.url.configSQL import Config

app = flask.Flask(__name__)
app.secret_key = "secret"
app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = Migrate(app, db)

import website.url.views

os.chdir("/home/elie/pythonprojects/website/url")
db.create_all()
