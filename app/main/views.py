# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Step, Project, User, Commit
from . import main
import json
from datetime import datetime


@main.route('/', methods=['GET'])
@login_required
def index():
    '''
    默认首页试图函数, 返回我参与的项目
    '''
    # print 'projects', current_user.projects
    p = current_user.projects.all()
    # print(p[0])
    if p == []:
        progress = 0
        finish_steps_length = 0
        steps_length = 0
        return render_template('project.html', project=None, projects=p,
                               progress=progress, finish_steps_length=finish_steps_length,
                               steps_length=steps_length, remained_days=None,  other_users=[])
    else:
        finish_steps_length = float(Step.query.filter_by(project_id=p[0].id, status=1).count())
    # finish_steps_length = float(len(list(finish_steps)))
        steps_length = float(len(list(p[0].steps)))
        progress = finish_steps_length / steps_length * 100
        remained_days = p[0].expected_finish_at - datetime.now()
        other_users = db.session.query(User).filter(User.id.notin_([u.id for u in p[0].users])).all()
        return render_template('project.html', project=p[0], projects=p,
                               progress=progress, finish_steps_length=finish_steps_length,
                               steps_length=steps_length, remained_days=remained_days,
                               other_users=other_users, commits=p[0].commits)


@main.route('/project/<project_id>', methods=['GET'])
@login_required
def project(project_id):
    '''
    项目显示细节
    '''
    # print 'projects', current_user.projects
    p = Project.query.get_or_404(project_id)
    finish_steps_length = Step.query.filter_by(project_id=p.id, status=1).count()
    steps_length = float(len(list(p.steps)))
    progress = finish_steps_length / steps_length * 100
    remained_days = p.expected_finish_at - datetime.now()
    other_users = db.session.query(User).filter(User.id.notin_([u.id for u in p.users])).all()
    # print [u.id for u in p.users], [u.id for u in other_users]
    return render_template('project.html', project=p, projects=current_user.projects.all(),
                           progress=progress, finish_steps_length=finish_steps_length,
                           steps_length=steps_length, remained_days=remained_days,
                           other_users=other_users, commits=p.commits)


@main.route('/step/finish/<id>', methods=['POST'])
@login_required
def finish_step(id):
    '''
    完成步骤
    '''
    remark = request.form.get('remark')
    p_status = 0
    s = Step.query.get_or_404(id)
    s.status = True
    s.finish_at = datetime.now()
    s.finish_remark = remark
    db.session.add(s)
    db.session.commit()
    p = s.project
    finish_steps_length = float(Step.query.filter_by(project_id=p.id, status=1).count())
    for i in p.steps:
        if i.status == False:
            break
    else:
        p.status = True
        p.finish_at = datetime.now()
        db.session.add(p)
        p_status = 1
    ret = {'p_status': p_status, 'sid': id, 'finish_steps_length': finish_steps_length}
    return json.dumps(ret)


@main.route('/create_project', methods=['POST'])
@login_required
def create_project():
    project_name = request.form.get('name')
    project_content = request.form.get('content')
    time = request.form.get('start_time')
    start_time = datetime.strptime(time, '%m/%d/%Y')
    time = request.form.get('finish_time')
    finish_time = datetime.strptime(time, '%m/%d/%Y')
    steps = []
    for i in range(1, len(request.form)-3):
        steps.append(request.form.get('step'+str(i)))
    p = Project(name=project_name, content=project_content, create_id=current_user.id,
                start_time=start_time, expected_finish_at=finish_time)
    db.session.add(p)
    db.session.commit()
    user =current_user._get_current_object()
    user.projects.append(p)
    db.session.add(user)
    for i in steps:
        s = Step(content=i, project=p)
        db.session.add(s)
    flash(u'创建成功')
    return redirect(url_for('main.project', project_id=p.id))


@main.route('/project/<project_id>/addUser', methods=['POST'])
@login_required
def add_user(project_id):
    # print project_id, request.form
    users_id = [r for r in request.form]
    # u = User.query.filter(id not in users_id).all()
    # print u
    p = Project.query.get_or_404(project_id)
    users = db.session.query(User).filter(User.id.in_(users_id)).all()
    # print users
    for u in users:
        p.users.append(u)
    db.session.add(p)
    flash(u'添加成功')
    return redirect(url_for('main.project', project_id=project_id))


@main.route('/project/step/<sid>/cancel')
@login_required
def step_status_cancel(sid):
    s = Step.query.get_or_404(sid)
    if s.project.creator == current_user:
        s.status = 0
        s.finish_remark = ''
        s.finish_at = None
        p = s.project
        db.session.add(s)
        if p.status == 1:
            p.status = 0
            p.finish_at = None
            db.session.add(p)
        return redirect(url_for('.project', project_id=s.project.id))


@main.route('/project/<project_id>/removeUser', methods=['POST'])
@login_required
def remove_user(project_id):
    p = Project.query.get_or_404(project_id)
    if p.creator == current_user:
        users_id = [r for r in request.form]
        users = db.session.query(User).filter(User.id.in_(users_id)).all()
        for u in users:
            p.users.remove(u)
    db.session.add(p)
    flash(u'移除成功')
    return redirect(url_for('main.project', project_id=project_id))


@main.route('/project/git/commit/<p_id>', methods=['POST'])
def git_commit(p_id):
    p = Project.query.get_or_404(p_id)
    data = json.loads(unicode(request.data))
    c = Commit(branch=data['branch'], ref=data['hashref'], cname=data['name'],
               cemail=data['email'], message=data['message'], project=p)
    db.session.add(c)
    return 'ok', 200
