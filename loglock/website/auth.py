from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import json


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
                #flash("Logged In Successfully", category='success')
                login_user(user, remember=True)
                if user.role == 'admin':
                    #return redirect('/admin')
                    return json.dumps({'result': 'success', 'message': 'login success'})
                elif user.role == 'teacher':
                    #return redirect('/teacher')
                    return json.dumps({'result': 'success', 'message': 'login success'})
                #return redirect(url_for('views.home'))
                return json.dumps({'result': 'success', 'message': 'login success'})
            else:
                #flash("Incorrect Password", category='error')
                return json.dumps({'result': 'error', 'message': 'Incorrect Password'})
        else:
            #flash("Email does not exist", category='error')
            return json.dumps({'result': 'error', 'message': 'Email does not exist'})

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        user = User.query.filter_by(email=email).first()
        if user:
            #flash("Email already exists", category='error')
            return json.dumps({'result': 'error', 'message': 'Email already exists'})
        elif len(email) < 6:
            #flash("Email must be greater than 11 characters", category='error')
            return json.dumps({'result': 'error', 'message': 'Email must be greater than 11 characters'})
        elif len(password) < 6:
            #flash("Passwords must be greater than 8 character", category='error')
            return json.dumps({'result': 'error', 'message': 'Passwords must be greater than 8 character'})
        if len(name) < 1:
            #flash("name must be greater than 1 character", category='error')
            return json.dumps({'result': 'error', 'message': 'name must be greater than 1 character'})
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'), name=name, role='user')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            #flash("Account Created!", category='success')
            #return redirect(url_for('views.home'))
            return json.dumps({'result': 'success', 'message': 'register success'})

    return render_template("register.html", user=current_user)

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
