# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import Required, Length, EqualTo
from ..models import User
from wtforms import ValidationError
from flask.ext.login import current_user


class LoginForm(Form):
    uid = StringField(u'工号', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'保持登陆状态')
    submit = SubmitField(u'登陆')


class RegisterForm(Form):

    uid = StringField(u'工号', validators=[Required(), Length(1, 64)])
    username = StringField(u'用户名', validators=[
                          Required(), Length(1, 64)])
    password = PasswordField(u'输入密码', validators=[
                          Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(u'重复密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(u'用户名已被注册过了。')


class EditForm(Form):
    uid = StringField(u'工号', validators=[Required(), Length(1, 10)])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64)])
    submit = SubmitField(u'确认修改')

    def validate_username(self, field):
        if field.data != current_user.name and User.query.filter_by(name=field.data).first():
            raise ValidationError(u'用户名已被注册过了。')


class ChangePasswdForm(Form):
    old_password = PasswordField(u'请输入密码', validators=[Required()])
    password = PasswordField(u'请输入新密码', validators=[
        Required(), EqualTo(u'password2', message='两次输入密码不一致')])
    password2 = PasswordField(u'重复新密码', validators=[Required()])
    submit = SubmitField(u'确认修改')


class ResetPassForm(Form):
    password = PasswordField(u'请输入新密码', validators=[
        Required(), EqualTo(u'password2', message='两次输入密码不一致')])
    password2 = PasswordField(u'重复新密码', validators=[Required()])
    submit = SubmitField(u'确认修改')

    
