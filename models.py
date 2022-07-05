from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

db = SQLAlchemy()
db_name = 'team_db.db'


class Workshops(db.Model):
    __tablename__ = 'workshops'

    wsh_id = db.Column('wsh_id', db.Integer, primary_key=True)
    wsh_name = db.Column('wsh_name', db.Text)
    date = db.Column('date', db.Text)

    def __init__(self, wsh_name, date):
        self.wsh_name = wsh_name
        self.date = date


class Grades(db.Model):
    __tablename__ = 'grades'
    # __table_args__ = (PrimaryKeyConstraint('wsh_id'),)

    evaluation_id = db.Column('evaluation_id', db.Integer, primary_key=True, autoincrement=True)
    wsh_id = db.Column('wsh_id', db.Integer, primary_key=False, unique=False)
    grade = db. Column('grade', db.Integer)

    def __init__(self, evaluation_id, wsh_id, grade):
        self.evaluation_id = evaluation_id
        self.wsh_id = wsh_id
        self.grade = grade
