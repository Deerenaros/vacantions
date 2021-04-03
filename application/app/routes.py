from flask import Flask, request, redirect
from sqlalchemy.orm import relationship, backref
from loguru import logger
from datetime import date, datetime
import names
import time
import psycopg2
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
        users = "<datalist id='users'>\n"
        for user in User.query.all():
            users += f"<option value='{user}'>\n"
        users += "</datalist>\n"

        result = f"""
        <form action="/" method="post">
            <input list="users" name="names" placeholder="Input Names Here">

            {users}

            <label for="leave">Leave date:</label>
            <input type="date" name="leave" id="leave" min="2021-01-01" max="2021-12-31">
            <label for="return">Return date:</label>
            <input type="date" name="return" id="return" min="2021-01-01" max="2021-12-31">
            <input type="submit">
        </form>
        """
        for user in User.query.all():
            result += f"<h3>{repr(user)}</h3>"
            for vac in user.vacantions:
                result += f"<p>from {vac.leave} to {vac.retrn} <a href='/{vac.id}'>X</a></p>"

        return result

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