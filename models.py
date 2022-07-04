from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

db = SQLAlchemy()
db_name = 'team_db.db'


class Workshops(db.Model):
    __tablename__ = 'workshops'

    wsh_id = db.Column('wsh_id', db.Integer, primary_key=True)
    wsh_name = db.Column('wsh_name', db.Text)

    def __init__(self, wsh_name):
        self.wsh_name = wsh_name


class Grades(db.Model):
    __tablename__ = 'grades'
    __table_args__ = (PrimaryKeyConstraint('wsh_id'),)

    wsh_id = db.Column('wsh_id', db.Integer, ForeignKey('workshops.wsh_id'))
    grade = db. Column('grade', db.Integer)

    def __init__(self, wsh_id, grade):
        self.wsh_id = wsh_id
        self.grade = grade
