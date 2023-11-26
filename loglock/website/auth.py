from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps


# Signup/Logins
auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In Successfully", category='success')
                login_user(user, remember=True)
                if user.role == 'admin':
                    return redirect('/admin')
                elif user.role == 'teacher':
                    return redirect('/teacher')
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash("Email does not exist", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        name = request.form.get('name')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category='error')
        elif len(email) < 6:
            flash("Email must be greater than 11 characters", category='error')
        elif password1 != password2:
            flash("Passwords dont match", category='error')
        elif len(password1) < 6:
            flash("Passwords must be greater than 8 character", category='error')
        elif len(name) < 1:
            flash("name must be greater than 1 character", category='error')
        else:
            new_user = User(email=email,password=generate_password_hash(password1, method='sha256'),name=name,role='user')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# 自定义鉴权装饰器,让不同角色的用户只能访问相应的接口或页面
def permission(permit_users):
    def login_acquired(func):
        @wraps(func)
        def inner():
            if current_user.role not in permit_users:
                return redirect('/login')   # 角色与页面不匹配跳转到登录页
            return func()
        return inner
    return login_acquired
