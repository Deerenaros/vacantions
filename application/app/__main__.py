import flask

from .db import init as init_db
from .routes import init as init_rt
from .ldap import init as populate


app = flask.Flask(__name__)
app["SECRET_KEY"] = b'GgqZe8SuG44Ex3D4CqC7BiTIY353ytL8'
init_db(app)
init_rt(app)
populate()