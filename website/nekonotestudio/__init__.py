__version__ = "1.0.0"
import sys, os

sys.path.append(os.path.abspath(os.path.curdir))
import flask
import flask_sqlalchemy
from flask_migrate import Migrate
from website.nekonotestudio.configSQL import Config

app = flask.Flask(__name__)
app.secret_key = "secret"
app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = Migrate(app, db)

# from website.nekonotestudio import views
from website.nekonotestudio import viewsruins

db.create_all()

if __name__ == "__main__":
    viewsruins.appruins.run(port=4999, debug=False)
