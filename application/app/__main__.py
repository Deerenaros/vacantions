import flask

from loguru import logger

from .db import init as init_db
from .routes import init as init_rt
from .ldap import init as populate


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = b'GgqZe8SuG44Ex3D4CqC7BiTIY353ytL8'
init_db(app)
logger.success("DB initialized")
init_rt(app)
logger.success("App initialized")
populate(app)
logger.success("DB populated")

from gevent import monkey
monkey.patch_all()

import os
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()