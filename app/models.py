# -*- coding: utf-8 -*-
from . import db, login_manager
from datetime import datetime
import uuid, time
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.exceptions import ValidationError


def next_id():
    '''
    结合时间戳产生50位随机id
    '''
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


registrations = db.Table('registrations',
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                         db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
                         )


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    content = db.Column(db.Text)
    status = db.Column(db.Boolean, default=0)
    start_time = db.Column(db.DateTime)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    expected_finish_at = db.Column(db.DateTime)
    finish_at = db.Column(db.DateTime, nullable=True)
    create_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    steps = db.relationship('Step', backref='project', lazy='dynamic')
    commits = db.relationship('Commit', backref='project', lazy='dynamic')
    priority = db.Column(db.Integer, default=0)
    records = db.relationship('Record', backref='project', lazy='dynamic')
    del_flag = db.Column(db.Boolean, default=False)
    father_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    father = db.relationship('Project', backref='children', remote_side=[id])
    git_name = db.Column(db.String(40), nullable=True)

    def __repr__(self):
        return '<Name {}>'.format(self.id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40))
    passwd = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=0)
    image_url = db.Column(db.String(500))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project',
                               secondary=registrations,
                               backref=db.backref('users', lazy='dynamic'),
                               lazy='dynamic')
    create_projects = db.relationship('Project',
                                      foreign_keys=[Project.create_id],
                                      backref=db.backref('creator', lazy='joined'),
                                      lazy='dynamic',
                                      cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passwd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwd, password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.name

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class Step(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.String(50), primary_key=True, default=next_id, unique=True)
    content = db.Column(db.Text)
    status = db.Column(db.Boolean, default=0)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    finish_at = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    finish_remark = db.Column(db.Text, nullable=True)
    del_flag = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Step {}>'.format(self.id)


class Commit(db.Model):
    __tablename__ = 'commits'

    id = db.Column(db.String(50), primary_key=True, default=next_id, unique=True)
    branch = db.Column(db.String(80))
    ref = db.Column(db.String(40))
    cname = db.Column(db.String(50))
    cemail = db.Column(db.String(50))
    message = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __repr__(self):
        return '<Step {}>'.format(self.id)


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.String(50), primary_key=True, default=next_id)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Record {}>'.format(self.id)
