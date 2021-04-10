from sqlalchemy.orm import relationship

from .db import db


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