# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app, request, flash
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Step, Project, User, Commit
from . import main
from .forms import ProjectForm
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


@main.route('/step/finish/<id>', methods=['GET'])
@login_required
def finish_step(id):
    '''
    完成步骤
    '''
    s = Step.query.get_or_404(id)
    s.status = True
    s.finish_at = datetime.now()
    db.session.add(s)
    db.session.commit()
    flash(u'操作成功')
    p = s.project
    for i in p.steps:
        if i.status == False:
            break
    else:
        p.status = True
        p.finish_at = datetime.now()
        db.session.add(p)
    return id


@main.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        project_name = request.form.get('name')
        project_content = request.form.get('content')
        time = request.form.get('start_time')
        create_at = datetime.strptime(time, '%m/%d/%Y')
        time = request.form.get('finish_time')
        finish_time = datetime.strptime(time, '%m/%d/%Y')
        steps = []
        for i in range(1, len(request.form)-3):
            steps.append(request.form.get('step'+str(i)))
        p = Project(name=project_name, content=project_content, create_id=current_user.id,
                    create_at=create_at, expected_finish_at=finish_time)
        db.session.add(p)
        user =current_user._get_current_object()
        user.projects.append(p)
        db.session.add(user)
        for i in steps:
            s = Step(content=i, project=p)
            db.session.add(s)
        flash(u'创建成功')
        return redirect(url_for('main.index'))
    return render_template('test.html')


@main.route('/project/<project_id>/addUser', methods=['POST'])
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


@main.route('/project/git/commit/<p_id>', methods=['POST'])
def git_commit(p_id):
    p = Project.query.get_or_404(p_id)
    data = json.loads(request.data)
    c = Commit(branch=data['branch'], ref=data['hashref'], cname=data['name'],
               cemail=data['email'], message=data['message'], project=p)
    db.session.add(c)
    return 'ok', 200