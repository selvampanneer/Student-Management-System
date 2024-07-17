from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, json, jsonify
from .models import Student, Faculty, Department, Course, Register, Instructor, Session, Status, Grade
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from . import db

adminAuth = Blueprint('adminAuth', __name__)
global access
access = False

global year
# year = 2026


year = datetime.now().year


@adminAuth.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_user = ""
    admin_password = ""
    if request.method == 'POST':
        name = request.form.get('adminUser')
        password = request.form.get('adminPassword')
        if name == admin_user and password == admin_password:
            flash('Admin logged in', category='success')
            global access
            access = True
            return redirect(url_for('adminAuth.admin', boolean=access))
        else:
            flash('Invalid admin credentials', category='error')

    return render_template("admin_features.html", boolean=access)


@adminAuth.route('/admin/f-features', methods=['GET', 'POST'])
def f_features():
    if access:

        if request.method == 'POST':

            if 'addFaculty' in request.form:
                dept = db.session.query(Department).all()
                selection = 'addFaculty'
                return render_template("f-features.html", boolean=access, feature=selection, group=dept)

            if 'submitFaculty' in request.form:
                first_name = request.form.get('firstName')
                last_name = request.form.get('lastName')
                department = request.form.get('dept')
                password1 = request.form.get('password1')
                # print(first_name, last_name, department)
                # faculty = Faculty.query.filter_by(first_name=first_name).first()
                num = Faculty.query.with_entities(func.max(Faculty.id)).scalar()
                reg_no = 'FC' + str(num + 1).zfill(4)
                # print(reg_no)
                # print(faculty)
                new_faculty = Faculty(id=num + 1, reg_no=reg_no, first_name=first_name, last_name=last_name,
                                      password=generate_password_hash(password1), dept_id=department)
                db.session.add(new_faculty)
                db.session.commit()
                # result = Faculty.query.filter_by(func.max(Student.id)).first()
                # print(result," in db")
                flash('Faculty Registered with Registration number: ' + reg_no, category='success')
                return redirect(url_for('adminAuth.f_features'))

            if 'allocateCourse' in request.form:
                # reg_no = request.form.get('reg_no').upper()
                # faculty = Faculty.query.filter_by(reg_no = reg_no).first()
                # if faculty is None:
                #     flash('Faculty does not exist', category='error')
                #     return redirect(url_for('adminAuth.f_features'))
                # courses = Course.query.filter_by(dept_id=faculty.dept_id).all()
                selection = 'allocateCourse'
                # print(dept)
                return render_template("f-features.html", boolean=access, feature=selection)

            if 'fetchCourses' in request.form:
                reg_no = request.form.get('reg_no').upper()
                faculty = Faculty.query.filter_by(reg_no=reg_no).first()
                if faculty is None:
                    flash('Faculty does not exist', category='error')
                    return redirect(url_for('adminAuth.f_features'))
                dept_id = Faculty.query.filter_by(id=faculty.id).first().dept_id
                # course for course in all_course if id not in instructor.c_id for instructor in Instructor.query.all()
                # courses = Course.query.filter_by(dept_id=faculty.dept_id) \
                #     .filter(~Course.id.in_(Instructor.query.with_entities(Instructor.c_id).distinct()))
                courses = Course.query.filter_by(dept_id=dept_id).all()
                ins = Instructor.query.with_entities(Instructor.c_id).distinct()
                final = []
                for course in courses:
                    # print(course)
                    flag = 0
                    for inst in ins:
                        # print(inst)
                        if inst[0] == course.id:
                            flag = 1
                    if flag == 0:
                        final.append(course)
                # print(final)
                selection = 'fetchCourses'
                return render_template("f-features.html", boolean=access, feature=selection, reg_no=reg_no,
                                       courses=final)
            if 'registerCourse' in request.form:
                reg_no = request.form.get('rno').upper()
                # print(reg_no)
                f_id = (Faculty.query.filter_by(reg_no=reg_no).first()).id
                # print(s_id)
                course_id = request.form.get('course')
                # print(course_id)
                # print(session_id)
                instruction = Instructor(f_id=f_id, c_id=course_id, year=year)
                # print(registration)
                db.session.add(instruction)
                db.session.commit()
                flash('Course allocated successfully', category='success')

            if 'viewFaculty' in request.form:
                selection = "viewFaculty"
                faculties = Faculty.query.filter_by().all()
                faculty_list = []
                for faculty in faculties:
                    if faculty.id == 10:
                        continue
                    faculty_data = {}
                    faculty_data['reg_no'] = faculty.reg_no
                    faculty_data['name'] = faculty.first_name + " " + faculty.last_name
                    faculty_data['dept'] = (Department.query.filter_by(id=faculty.dept_id).first()).dept_name
                    instructs = Instructor.query.join(Faculty).filter(Instructor.f_id == faculty.id)
                    course_ids = (Course.query.filter_by(id=course).first() for course in
                                  (instruct.c_id for instruct in instructs))
                    faculty_data['course_ids'] = course_ids
                    faculty_list.append(faculty_data)
                return render_template("f-features.html", boolean=access, feature=selection,
                                       faculty_list=faculty_list)

        return render_template("f-features.html", boolean=access)

    else:
        return redirect(url_for('adminAuth.admin'))


@adminAuth.route('/admin/s-features', methods=['GET', 'POST'])
def s_features():
    if access:
        if request.method == 'POST':

            if 'addStudent' in request.form:
                dept = db.session.query(Department).all()
                selection = 'addStudent'
                return render_template("s-features.html", boolean=access, feature=selection, group=dept)

            if 'submitStudent' in request.form:
                first_name = request.form.get('firstName')
                last_name = request.form.get('lastName')
                department = request.form.get('dept')
                password1 = request.form.get('password1')
                # print(first_name, last_name, department)
                current_year = str(year % 100)
                # faculty = Faculty.query.filter_by(first_name=first_name).first()
                num = db.session.query(func.max(Student.id)).filter(Student.reg_no.like(f'{current_year}%')).scalar()
                if num is None:
                    num = 100
                reg_no = current_year + 'US' + str(num + 1).zfill(4)
                # print(reg_no)
                # print(faculty)
                new_student = Student(reg_no=reg_no, first_name=first_name, last_name=last_name,
                                      password=generate_password_hash(password1), dept_id=department)
                db.session.add(new_student)
                db.session.commit()
                # result = Faculty.query.filter_by(func.max(Student.id)).first()
                # print(result," in db")
                flash('Student Registered with Registration number: ' + reg_no, category='success')
                return redirect(url_for('adminAuth.s_features'))

            if 'allocateCourse' in request.form:
                dept = Department.query.filter_by().all()
                selection = 'allocateCourse'
                # print(dept)
                return render_template("s-features.html", boolean=access, feature=selection, group=dept)

            if 'fetchDepartment' in request.form:
                reg_no = request.form.get('reg_no').upper()
                if Student.query.filter_by(reg_no=reg_no).first() is None:
                    flash('Student does not exist', category='error')
                    return redirect(url_for('adminAuth.s_features'))
                student = Student.query.filter_by(reg_no=reg_no).first()
                dept = request.form.get('department')
                # print(dept)
                selection = 'fetchDepartment'
                courses = Course.query.filter_by(dept_id=dept,status_id=1) \
                    .filter(Course.id.in_(Instructor.query.with_entities(Instructor.c_id).distinct()))
                registered_courses = Course.query.filter(Course.id.in_(register.c_id for register in
                                                                       Register.query.filter_by(
                                                                           s_id=student.id).all())).all()

                registered_ids = [course.id for course in registered_courses]
                courses = courses.filter(~Course.id.in_(registered_ids))

                return render_template("s-features.html", boolean=access, feature=selection, reg_no=reg_no,
                                       group=(Department.query.filter_by(id=dept).first()).dept_name, courses=courses)

            if 'registerCourse' in request.form:
                reg_no = request.form.get('rno').upper()
                # print(reg_no)
                s_id = (Student.query.filter_by(reg_no=reg_no).first()).id
                # print(s_id)
                course_id = request.form.get('course')
                # print(course_id)
                # print(session_id)
                registration = Register(s_id=s_id, c_id=course_id, year=year)
                # print(registration)
                db.session.add(registration)
                db.session.commit()
                flash('Course allocated successfully', category='success')

            if 'viewStudents' in request.form:
                selection = "viewStudents"
                students = Student.query.filter_by().all()
                student_list = []
                for student in students:
                    if student.id == 100:
                        continue
                    student_data = {}
                    student_data['reg_no'] = student.reg_no
                    student_data['name'] = student.first_name + " " + student.last_name
                    student_data['dept'] = (Department.query.filter_by(id=student.dept_id).first()).dept_name
                    registrations = Register.query.join(Student).filter(Register.s_id == student.id)
                    course_ids = list(Course.query.filter_by(id=course).first() for course in
                                      (register.c_id for register in registrations))
                    sessions = list(Session.query.filter_by(id=session_id).first().session for session_id in
                                    (course.session_id for course in course_ids))
                    years = [register.year for register in registrations]
                    student_data['course_ids'] = course_ids
                    student_data['sessions'] = sessions
                    student_data['years'] = years
                    student_list.append(student_data)
                return render_template("s-features.html", boolean=access, feature=selection, student_list=student_list,
                                       zip=zip)

        return render_template("s-features.html", boolean=access)

    else:
        return redirect(url_for('adminAuth.admin'))


@adminAuth.route('/admin/c-features', methods=['GET', 'POST'])
def c_features():
    if access:
        if request.method == 'POST':
            if 'addCourse' in request.form:
                dept = Department.query.filter_by().all()
                sessions = Session.query.filter_by().all()
                selection = 'addCourse'
                return render_template("c-features.html", boolean=access, feature=selection, dept=dept,
                                       sessions=sessions)

            if 'submitCourse' in request.form:
                course_name = request.form.get('name')
                dept_id = request.form.get('department')
                session = request.form.get('session')
                session_id = int(session)
                # print(session)
                max_c_id = Course.query.filter_by(dept_id=dept_id).with_entities(func.max(Course.id)).scalar()
                if not max_c_id:
                    max_c_id = int(dept_id +'09')
                new_course = Course(id=max_c_id + 1, name=course_name.title(), dept_id=dept_id, session_id=session_id,
                                    )
                db.session.add(new_course)
                db.session.commit()
                generated_id = "C" + str(max_c_id + 1)
                flash('Course added successfully :: Generated Course id: ' + generated_id, category='success')
                return redirect(url_for('adminAuth.c_features'))

            if 'viewCourses' in request.form:
                courses = Course.query.filter_by().all()
                status = Status.query.filter_by().all()
                selection = 'viewCourses'
                data = []
                for course in courses:
                    row = {}
                    row['name'] = course.name
                    row['id'] = course.id
                    department = Department.query.filter_by(id=course.dept_id).first()
                    session = Session.query.filter_by(id=course.session_id).first()
                    instruct = Instructor.query.filter_by(c_id=course.id).first()
                    strength = Register.query.filter_by(c_id=course.id).with_entities(func.count()).scalar()
                    course_status = Status.query.filter_by(status_id=course.status_id).first()
                    # print(status.status)
                    if instruct:
                        faculty = Faculty.query.filter_by(id=instruct.f_id).first()
                        row['instructor'] = "Prof. " + faculty.first_name + " " + faculty.last_name
                    else:
                        row['instructor'] = "Not Assigned"
                    row['dept_name'] = department.dept_name
                    row['session'] = session.session
                    row['strength'] = strength
                    row['course_status'] = course_status
                    # row['status'] = status
                    data.append(row)
                return render_template("c-features.html", boolean=access, feature=selection, courses=data,
                                       status=status)

            if 'saveStatus' in request.form:
                selection = 'viewCourses'
                course = request.form.get('saveStatus')
                course = Course.query.filter_by(id=int(course)).first()
                option = request.form.get(f'status_{course.id}')
                status = Status.query.filter_by(status_id=option).first()
                course.status_id = option
                db.session.commit()
                # print(course.status_id)
                # for key in request.form:
                #     if key.startswith('course_id_'):
                #         course_id = request.form.get(key)
                #         print(course_id)
                flash(f'C{course.id} - {course.name} : {status.status}', category='success')
                return redirect(url_for('adminAuth.c_features'))
        return render_template("c-features.html", boolean=access)
    else:
        return redirect(url_for('adminAuth.admin'))


@adminAuth.route('/admin/g-features', methods=['GET', 'POST'])
def g_features():
    if access:
        if request.method == 'POST':
            if 'saveStatus' in request.form:
                course = request.form.get('saveStatus')
                course = Course.query.filter_by(id=int(course)).first()
                option = request.form.get(f'status_{course.id}')
                status = Status.query.filter_by(status_id=option).first()
                course.status_id = option
                db.session.commit()
                flash(f'C{course.id} - {course.name} : {status.status}', category='success')
                return redirect(url_for('adminAuth.g_features'))
        # if request.method == 'GET':
        selection = ""
        courses = Course.query.filter_by().all()
        status = Status.query.filter_by().all()
        data = []
        for course in courses:
            instruct = Instructor.query.filter_by(c_id=course.id).first()
            strength = Register.query.filter_by(c_id=course.id, year=year).with_entities(func.count()).scalar()
            # print(strength)
            if instruct and strength:
                row = {}
                row['name'] = course.name
                row['id'] = course.id
                department = Department.query.filter_by(id=course.dept_id).first()
                session = Session.query.filter_by(id=course.session_id).first()
                instruct = Instructor.query.filter_by(c_id=course.id).first()
                faculty = Faculty.query.filter_by(id=instruct.f_id).first()
                course_status = Status.query.filter_by(status_id=course.status_id).first()
                row['instructor'] = "Prof. " + faculty.first_name + " " + faculty.last_name
                row['dept_name'] = department.dept_name
                row['session'] = session.session
                row['strength'] = strength
                row['course_status'] = course_status
                data.append(row)
        return render_template("g-features.html", boolean=access, feature=selection, courses=data, status=status)


    else:
        return redirect(url_for('adminAuth.admin'))


@adminAuth.route('/admin/logout')
def logout():
    global access
    access = False
    return redirect(url_for('userAuth.login'))
