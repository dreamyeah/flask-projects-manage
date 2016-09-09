#!/usr/bin/env python
# coding=utf-8
import os
from app import create_app, db
from app.models import Step, User, Project, Commit, Record, registrations
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.template_filter('date_output')
def datetime_filter(dt):
    '''
    :param dt: datetime
    :return: 年月日输出
    '''
    return dt.strftime('%Y-%m-%d')


@app.template_filter('days_output')
def days_filter(timedelte):
    '''
    :param timedelte: 时间差 类型：datetime.timedelte
    :return: 按需输出
    '''
    return timedelte.days


@app.template_filter('negate')
def negate_filter(d):
    '''
    :param d: int
    :return: -d
    '''
    return -d

@app.template_filter('formatSize')
def formatSize(d):
    '''
    :param d: int
    :return: str
    '''
    if d < 1024:
        return str(d) +' B'
    elif d < 1024*1024:
        return str(d/1024) + ' KB'
    elif d < 1024*1024*1024:
        return str(d/(1024*1024)) + ' MB'
    else:
        return str(d/(1024*1024*1024)) + ' GB'


def make_shell_context():
    return dict(app=app, db=db, Step=Step, User=User, Project=Project, Commit=Commit, Record=Record, registrations=registrations)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
