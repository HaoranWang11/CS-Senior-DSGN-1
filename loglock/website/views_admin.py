import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User
from .models import Attendance
from .models import CheckinPWD
from .auth import permission


# Website URLS (Routes)
views_admin = Blueprint('views_admin',__name__)

# Main Page
@views_admin.route('/admin')
@views_admin.route('/admin/admin_home')
@login_required
@permission(['admin'])
def admin_home():
    page = request.args.get("page")
    if page is None:
        page = 1
    else:
        page = int(page)
    limit = request.args.get("limit")
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    checkinpwds = CheckinPWD.query.paginate(page=page, per_page=limit)
    return render_template("admin_home.html", user=current_user, checkinpwds=checkinpwds)

@views_admin.route('/admin/add_check_in_pwd', methods = ['POST'])
@login_required
@permission(['admin'])
def admin_add_check_in_pwd():
    pwd = request.form.get("pwd")
    if pwd is None:
        return '{"result":0, "msg":"params error!"}'
    if CheckinPWD.query.filter_by(pwd=pwd).first():
        return '{"result":0, "msg":"Check-in password already exists!"}'
    new_checkinpwd = CheckinPWD(pwd=pwd)
    db.session.add(new_checkinpwd)
    db.session.commit()
    return '{"result":200, "msg":"success!"}'

@views_admin.route('/admin/delete_check_in_pwd', methods = ['POST'])
@login_required
@permission(['admin'])
def admin_delete_check_in_pwd():
    a_id = request.form.get("id")
    if a_id is None:
        return '{"result":0, "msg":"params error!"}'
    CheckinPWD.query.filter(CheckinPWD.id==a_id).delete()
    db.session.commit()
    return '{"result":200, "msg":"success!"}'

@views_admin.route('/admin/attendance_by_pwd')
@login_required
@permission(['admin'])
def admin_attendance_by_pwd():
    pwd = request.args.get("pwd")
    if pwd is None:
        return redirect('/admin')

    page = request.args.get("page")
    if page is None:
        page = 1
    else:
        page = int(page)
        if page == 0:
            page = 1
    limit = request.args.get("limit")
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    attendances = Attendance.query.filter(Attendance.pwd==pwd).paginate(page=page, per_page=limit)
    return render_template("admin_attendance_by_pwd.html", user=current_user, attendances=attendances, pwd=pwd)

@views_admin.route('/admin/attendance_by_time_start')
@login_required
@permission(['admin'])
def admin_attendance_by_time_start():
    select_time = request.args.get("t")
    if select_time is not None:
        t1 = datetime.datetime.strptime(select_time,'%Y-%m-%d')
    else:
        t1 = datetime.datetime.today()
    t2 = datetime.time(0, 0, 0)
    t3 = datetime.time(23, 59, 59)
    start = datetime.datetime.combine(t1, t2)
    end = datetime.datetime.combine(t1, t3)
    attendance_list = Attendance.query.filter(Attendance.attendance_time.between(start, end)).all()
    return redirect('/admin/attendance_by_time?t=%04d-%02d-%02d'%(t1.year,t1.month,t1.day))

@views_admin.route('/admin/attendance_by_time')
@login_required
@permission(['admin'])
def admin_attendance_by_time():
    select_time = request.args.get("t")
    if select_time is not None:
        t1 = datetime.datetime.strptime(select_time,'%Y-%m-%d')
    else:
        t1 = datetime.datetime.today()
    t2 = datetime.time(0, 0, 0)
    t3 = datetime.time(23, 59, 59)
    start = datetime.datetime.combine(t1, t2)
    end = datetime.datetime.combine(t1, t3)
    curr_t = '%04d-%02d-%02d' % (t1.year,t1.month,t1.day)

    page = request.args.get("page")
    if page is None:
        page = 1
    else:
        page = int(page)
        if page == 0:
            page = 1
    limit = request.args.get("limit")
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    attendances = Attendance.query.filter(Attendance.attendance_time.between(start, end)).paginate(page=page, per_page=limit)
    return render_template("admin_attendance_by_time.html", user=current_user, attendances=attendances, curr_t=curr_t)

@views_admin.route('/admin/delete_attendance', methods = ['POST'])
@login_required
@permission(['admin'])
def admin_delete_attendance():
    a_id = request.form.get("id")
    if a_id is None:
        return '{"result":0, "msg":"params error!"}'
    Attendance.query.filter(Attendance.id==a_id).delete()
    db.session.commit()
    return '{"result":200, "msg":"success!"}'

@views_admin.route('/admin/account_management')
@login_required
@permission(['admin'])
def admin_account_management():
    page = request.args.get("page")
    if page is None:
        page = 1
    else:
        page = int(page)
    limit = request.args.get("limit")
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    users = User.query.paginate(page=page, per_page=limit)
    return render_template("admin_account_management.html", user=current_user, users=users)

@views_admin.route('/admin/delete', methods = ['POST'])
@login_required
@permission(['admin'])
def admin_delete():
    email = request.form.get("e")
    if email is None:
        return '{"result":0, "msg":"params error!"}'
    if email == 'admin':
        return '{"result":0, "msg":"params error!"}'
    User.query.filter(User.email==email).delete()
    db.session.commit()
    return '{"result":200, "msg":"success!"}'

@views_admin.route('/admin/change_role', methods = ['POST'])
@login_required
@permission(['admin'])
def admin_change_role():
    email = request.form.get("e")
    if email is None:
        return '{"result":0, "msg":"params error!"}'
    if email == 'admin':
        return '{"result":0, "msg":"params error!"}'
    role = request.form.get("r")
    if role is None:
        return '{"result":0, "msg":"params error!"}'
    User.query.filter(User.email==email).update({'role' : role})
    db.session.commit()
    return '{"result":200, "msg":"success!"}'

@views_admin.route('/admin/grade_management')
@login_required
@permission(['admin'])
def admin_grade_management():
    query_email = request.args.get("email")
    if query_email is None:
        query_email = ""

    page = request.args.get("page")
    if page is None:
        page = 1
    else:
        page = int(page)
    limit = request.args.get("limit")
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    users = User.query.filter(User.email.ilike(f"%{query_email}%")).paginate(page=page, per_page=limit)
    return render_template("admin_grade_management.html", user=current_user, users=users, query_email=query_email)
