from sqlalchemy import CheckConstraint

from . import db
from flask_login import UserMixin


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    grade = db.Column(db.String(3))
    grade_point = db.Column(db.Integer, CheckConstraint('grade_point>=0 AND grade_point<=10'))
    grade_information = db.Column(db.String(50))


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status_id = db.Column(db.Integer, CheckConstraint('status>=0 AND status<=3'))
    status = db.Column(db.String(50))


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_name = db.Column(db.String(100))
    courses = db.relationship('Course')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dept_id = db.Column(db.String(100), db.ForeignKey('department.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), default=0)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(7), nullable=False)


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    c_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    year = db.Column(db.Integer, CheckConstraint('year >= 2024 AND year <= 2100'))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), default=1)
    # registration = db.relationship('Student')


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    c_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    year = db.Column(db.Integer, CheckConstraint('year >= 2024 AND year <= 2100'))


class Faculty(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(8), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(150))
    dept_id = db.Column(db.String(100), db.ForeignKey('department.id'))
    instruct = db.relationship('Instructor')


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(8), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    dept_id = db.Column(db.String(100), db.ForeignKey('department.id'))
    registration = db.relationship('Register')
