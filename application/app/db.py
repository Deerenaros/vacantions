import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .model import *


def init(app):
    from utils import postgres_test

    dbname = os.environ.get("DBNAME", "db")
    dbhost = os.environ.get("DBHOST", "db")
    dbuser = os.environ.get("DBUSER", "user")
    dbpswd = os.environ.get("DBPSWD", "user")
    dbdrvr = os.environ.get("dbdrvr", "postgresql+psycopg2")

    tries = 0
    while not postgres_test(dbname, dbhost, dbuser, dbpswd):
        time.sleep(1)
        if (tries := tries + 1) > 10:
            raise Exception("No database connection available")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"{dbdrvr}://{dbuser}:{dbpswd}@{dbhost}/{dbname}"
    db.init_app(app)

    db.drop_all()
    db.create_all()