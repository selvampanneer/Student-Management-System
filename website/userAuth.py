from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash

userAuth = Blueprint('userAuth', __name__)
from .models import Student, Faculty
from flask_login import login_user, login_required, current_user, logout_user


@userAuth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        reg_no = request.form.get('reg_no').upper()
        password = request.form.get('password')
        # print(reg_no[2:4])
        # if reg_no[0:2] == 'us':
        #     print(reg_no[0:2])
        # print("over")
        if len(reg_no) < 6:
            flash('Invalid Registration number', category='error')
        elif len(password) < 2:
            flash('Invalid password', category='error')

        elif reg_no[0:2] == "FC":
            faculty = Faculty.query.filter_by(reg_no=reg_no).first()
            if faculty:
                if check_password_hash(faculty.password, password):
                    flash('Welcome ' + faculty.first_name + '!', category='success')
                    login_user(faculty, remember=True)
                    session['type'] = 'faculty'
                    return redirect(url_for('views.faculty_dashboard'))
                else:
                    flash('Incorrect password', category='error')
            else:
                flash('Invalid Registration number,', category='error')

        elif reg_no[2:4] == "US":
            student = Student.query.filter_by(reg_no=reg_no).first()
            if student:
                if check_password_hash(student.password, password):
                    flash('Welcome ' + student.first_name + '!', category='success')
                    login_user(student, remember=True)
                    session['type'] = 'student'
                    return redirect(url_for('views.student_dashboard'))
                else:
                    flash('Incorrect password', category='error')
            else:
                flash('Ivalid Registration number,', category='error')
        else:
            flash('Registration number does not exist,', category='error')
    return render_template("login.html")


@userAuth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('userAuth.login'))
