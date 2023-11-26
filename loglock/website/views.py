
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Attendance
from .models import CheckinPWD
import datetime


# Website URLS (Routes)
views = Blueprint('views',__name__)

# Main Page
@views.route('/')
@login_required
def home():
    if current_user.role == 'admin':
        return redirect(url_for('views_admin.admin_home'))
    elif current_user.role == 'teacher':
        return redirect(url_for('views_teacher.teacher_home'))

    attendances = Attendance.query.filter(Attendance.email==current_user.email).order_by(Attendance.attendance_time.desc()).paginate(page=1, per_page=10)
    return render_template("user_home.html", user=current_user, attendances=attendances)

@views.route('/attendance', methods = ['POST'])
@login_required
def attendance():
    pwd = request.form.get("pwd")
    if pwd is None:
        return '{"result":0, "msg":"params error!"}'
    if not CheckinPWD.query.filter_by(pwd=pwd).first():
        return '{"result":0, "msg":"No such check-in password!"}'
    attendance = Attendance.query.filter(Attendance.email==current_user.email,Attendance.pwd==pwd).first()
    if attendance:
        return '{"result":0, "msg":"You have completed the check-in process!"}'
    new_attendance = Attendance(email=current_user.email, name=current_user.name, pwd=pwd)
    db.session.add(new_attendance)
    db.session.commit()
    return '{"result":200, "msg":"success!"}'

# More Information About Page
@views.route('/about')
def about():
    return render_template("about.html", user=current_user)
