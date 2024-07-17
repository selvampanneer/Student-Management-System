from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, distinct
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import Faculty, Department, Register, Instructor, Course, Session, Status, Grade, Student

views = Blueprint('views', __name__)
global year
year = datetime.now().year
# year = 2025


@views.route('/faculty_dashboard')
@login_required
def faculty_dashboard():
    instructions = []

    for record in current_user.instruct:
        instruction = {}
        course = Course.query.filter_by(id=record.c_id).first()
        instruction['course_id'] = course.id
        instruction['course_name'] = course.name
        instruction['session'] = (Session.query.filter_by(id=course.session_id).first()).session
        instruction['year'] = record.year
        instruction['strength'] = Register.query.filter_by(c_id=course.id, year=year).with_entities(
            func.count()).scalar()
        instruction['status'] = Status.query.filter_by(status_id=course.status_id).first()
        instructions.append(instruction)
    # print(instructions)
    return render_template("faculty_dashboard.html", user=current_user,
                           dept=Department.query.filter_by(id=current_user.dept_id).first(), instructions=instructions)


@views.route('/faculty_dashboard/<course_id>/view_batch', methods=['GET', 'POST'])
@login_required
def view_batch(course_id):
    if request.method == 'POST':
        if 'viewotherBatches' in request.form:
            distinct_years = db.session.query(distinct(Register.year)).all()
            years = [year[0] for year in distinct_years]
            get_year = request.form.get('year')
            batch = Register.query.filter_by(year=get_year, c_id=course_id).all()
            students = []
            for entry in batch:
                student = Student.query.filter_by(id=entry.s_id).first()
                info = {}
                info['reg_no'] = student.reg_no
                info['name'] = student.first_name + " " + student.last_name
                students.append(info)
            return render_template("view_batch.html", user=current_user,
                                   dept=Department.query.filter_by(id=current_user.dept_id).first(),
                                   batch=students, year=get_year, years=years)
    batch = Register.query.filter_by(c_id=course_id, year=year).all()
    students = []
    distinct_years = db.session.query(distinct(Register.year)).all()
    years = [g_year[0] for g_year in distinct_years]
    for entry in batch:
        student = Student.query.filter_by(id=entry.s_id).first()
        info = {'reg_no': student.reg_no, 'name': student.first_name + " " + student.last_name}
        students.append(info)
    return render_template("view_batch.html", user=current_user,
                           dept=Department.query.filter_by(id=current_user.dept_id).first(),
                           batch=students, year=year, years=years)


@views.route('/faculty_dashboard/<course_id>/grade_assigner', methods=['GET', 'POST'])
@login_required
def grade_assigner(course_id):
    if request.method == 'POST':
        if 'assignGrade' in request.form:
            selection = 'assignGrade'
            register = request.form.get('assignGrade')
            register = Register.query.filter_by(id=int(register)).first()
            grade = request.form.get(f'grade_{register.id}')
            student = Student.query.filter_by(id=register.s_id).first()
            register.grade_id = grade
            db.session.commit()
            flash(f'Grade saved for Student - {student.reg_no}', category='success')
            return redirect(url_for('views.grade_assigner', course_id=course_id))

        if 'submitGrade' in request.form:
            course = request.form.get('submitGrade')
            course = Course.query.filter_by(id=course).first()
            course.status_id += 1
            db.session.commit()
            status = Status.query.filter_by(id=course.status_id + 1).first()
            flash(f'Course C{course.id} : {status.status}', category='success')
            return redirect(url_for('views.faculty_dashboard'))

    # if request.method == 'GET':
    batch = Register.query.filter_by(c_id=course_id, year=year).all()
    students = []
    for entry in batch:
        student = Student.query.filter_by(id=entry.s_id).first()
        grade_list = Grade.query.filter_by().all()
        grade_list = sorted(grade_list, key=lambda x: x.id, reverse=True)
        info = {}
        info['id'] = entry.id
        info['reg_no'] = student.reg_no
        info['name'] = student.first_name + " " + student.last_name
        info['grade'] = Grade.query.filter_by(id=entry.grade_id).first()
        students.append(info)
    return render_template("grade_assigner.html", user=current_user,
                           dept=Department.query.filter_by(id=current_user.dept_id).first(), course_id=course_id,
                           batch=students, grade_list=grade_list)


@views.route('/student_dashboard')
@login_required
def student_dashboard():
    registrations = []
    window = {}
    count = 0
    # current_user = Student.query.filter_by(id=101).first()
    if current_user.registration:
        window['register_window'] = "show"
    else:
        window['register_window'] = "hide"

    for record in current_user.registration:
        registration = {}
        course = Course.query.filter_by(id=record.c_id).first()
        registration['course_id'] = course.id
        registration['course_name'] = course.name
        faculty = Faculty.query.join(Instructor).filter(Instructor.c_id == record.c_id).first()
        # faculty = Faculty.query.filter_by(id=(Instructor.query.filter_by(c_id=record.c_id).first()).f_id).first()
        registration['course_instructor'] = "Prof. " + faculty.first_name + " " + faculty.last_name
        registration['course_status'] = (Status.query.filter_by(status_id=course.status_id).first()).status
        registration['session'] = (Session.query.filter_by(id=course.session_id).first()).session
        registration['year'] = record.year
        if registration['course_status'] == "Completed for this Session":
            window['grading_window'] = "show"
            count += 1
            registration['grade'] = (Grade.query.filter_by(id=record.grade_id).first()).grade
        registrations.append(registration)

    if not count:
        window['grading_window'] = "hide"

    return render_template("student_dashboard.html", user=current_user,
                           dept=Department.query.filter_by(id=current_user.dept_id).first(),
                           registrations=registrations, window=window)


@views.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        if "change_password" in request.form:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            if current_password == new_password:
                flash('Please use a different Password ', category='error')
                return redirect(url_for('views.faculty_dashboard'))
            # current_password = generate_password_hash(current_password)
            # print(current_user.password)
            if check_password_hash(current_user.password, current_password):
                if new_password == confirm_password:
                    current_user.password = generate_password_hash(confirm_password)
                    db.session.commit()
                    flash('Password Changed Successfully. Please Login Again!', category='success')
                    return redirect(url_for('userAuth.logout', user=current_user))
                else:
                    flash('New passwords do not match', category='error')
            else:
                flash('Current password is Incorrect', category='error')
            # print(current_password, confirm_password, new_password)

    return redirect(url_for('views.faculty_dashboard'))
