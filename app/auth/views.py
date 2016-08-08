# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm, EditForm, ChangePasswdForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.uid.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'错误的用户名或密码.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(id=form.uid.data,
                    name=form.username.data.strip(),
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'注册成功!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        user.name = form.username.data
        db.session.add(user)
        db.session.commit()
        flash(u'用户名修改成功')
        return redirect(url_for('.edit'))
    form.uid.data = current_user.id
    form.username.data = current_user.name
    return render_template('auth/edit.html', form=form)


@auth.route('/changepasswd', methods=['POST', 'GET'])
def change_passwd():
    form = ChangePasswdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('输入密码错误')
    return render_template('auth/change_passwd.html', form=form)


def allowed_file(filename):
    '''
    判断文件格式
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif'])



