from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from loguru import logger
from datetime import date, datetime
import names

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:user@db/db'
db = SQLAlchemy(app)

class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    leave = db.Column(db.Date)
    retrn = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    mid_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)

    vacantions = relationship("Vacation", backref=("user"))

    def __repr__(self):
        return '[User %r %r %r]' % (self.first_name, self.mid_name, self.last_name)

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.mid_name, self.last_name)

db.drop_all()
db.create_all()

for i in range(0, 500):
    logger.error(i)
    user = User(first_name=names.get_first_name(), mid_name=names.get_first_name(gender='male'), last_name=names.get_last_name())
    db.session.add(user)

db.session.commit()


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
            result += f"<p>from {vac.leave} to {vac.retrn}</p>"

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