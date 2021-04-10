from flask import Flask, request, redirect, render_template
from sqlalchemy.orm import relationship, backref
from loguru import logger
from datetime import date, datetime
import time
import os

from .model import *


def init(app):
    @app.route("/<int:id>", methods=["GET"])
    def removevacation(id):
        Vacation.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect("/")

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.j2", users=User.query.all())

    @app.route("/", methods=["POST"])
    def post():
        logger.error(request.form)
        first, mid, last = request.form.get("names").split(" ")
        user = User.query.filter_by(first_name=first, mid_name=mid, last_name=last).first()
        leave = datetime.strptime(request.form.get("leave"), "%Y-%m-%d").date()
        retrn = datetime.strptime(request.form.get("return"), "%Y-%m-%d").date()
        vctn = Vacation(leave=leave, retrn=retrn)   
        user.vacantions.append(vctn)
        db.session.commit()
        return redirect("/")