from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from loguru import logger
from datetime import date, datetime
import names
import time
import psycopg2
import os
import ldap

dbname = os.environ.get("DBNAME", "db")
dbhost = os.environ.get("DBHOST", "db")
dbuser = os.environ.get("DBUSER", "user")
dbpswd = os.environ.get("DBPSWD", "user")
dbdrvr = os.environ.get("dbdrvr", "postgresql+psycopg2")

ldapuri = os.environ.get("LDAPURI")
ldapbase = os.environ.get("LDAPBASE")
ldapbind = os.environ.get("LDAPBIND")
ldappswd = os.environ.get("LDAPPSWD")


def postgres_test():
    try:
        conn = psycopg2.connect(f"dbname='{dbname}' user='{dbuser}' host='{dbhost}' password='{dbpswd}' connect_timeout=1")
        conn.close()
        return True
    except:
        return False

tries = 0
while not postgres_test():
    time.sleep(1)
    if (tries := tries + 1) > 10:
        raise Exception("No database connection available")

ldap_conn = ldap.initialize(ldapuri)
ldap_conn.simple_bind_s(ldapbind, ldappswd)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"{dbdrvr}://{dbuser}:{dbpswd}@{dbhost}/{dbname}"
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


searchFilter = "(objectClass=*)"
searchAttribute = ["givenname","sn"]
searchScope = ldap.SCOPE_SUBTREE
ldaprslt = ldap_conn.search(ldapbase, searchScope, searchFilter, searchAttribute)

try:
    ldap_result_id = ldap_conn.search(ldapbase, searchScope, searchFilter, searchAttribute)
    result_set = []
    while 1:
        result_type, result_data = ldap_conn.result(ldap_result_id, 0)
        if (result_data == []):
            break
        else:
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)
    print(result_set)
    for entry in result_set[1:]:
        print(entry)
        user = User(first_name=entry[0][1]["givenName"][0].decode("utf-8"), mid_name="", last_name=entry[0][1]["sn"][0].decode("utf-8"))
        db.session.add(user)
except ldap.LDAPError as e:
    import traceback
    traceback.print_tb(e)

#for i in range(0, 50):
#    logger.error(i)
#    user = User(first_name=names.get_first_name(), mid_name=names.get_first_name(gender='male'), last_name=names.get_last_name())
#    db.session.add(user)

db.session.commit()

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