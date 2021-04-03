import flask

from .db import init as init_db
from .routes import init as init_rt
from .ldap import init as populate


app = flask.Flask(__name__)
init_db(app)
init_rt(app)
populate()