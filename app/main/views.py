# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Step, Project, User, Commit, Record
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
    if current_user.admin:
        p = Project.query.order_by(Project.priority.desc()).all()
    else:
        p = current_user.projects.order_by(Project.priority.desc()).all()
    # print(p[0])
    if p == []:
        progress = 0
        finish_steps_length = 0
        steps_length = 0
        return render_template('project.html', project=None, projects=p,
                               progress=progress, finish_steps_length=finish_steps_length,
                               steps_length=steps_length, remained_days=None, other_users=[])
    else:
        color = ['info', 'info', 'info', 'warning', 'warning', 'warning']
        finish_steps_length = float(Step.query.filter_by(project_id=p[0].id, status=1).count())
        # finish_steps_length = float(len(list(finish_steps)))
        steps_length = float(len(list(p[0].steps)))
        progress = finish_steps_length / steps_length * 100
        remained_days = p[0].expected_finish_at - datetime.now()
        other_users = db.session.query(User).filter(User.id.notin_([u.id for u in p[0].users])).all()
        return render_template('project.html', project=p[0], projects=p,
                               progress=progress, finish_steps_length=finish_steps_length,
                               steps_length=steps_length, remained_days=remained_days,
                               other_users=other_users, commits=p[0].commits,
                               color=color)


@main.route('/project/<project_id>', methods=['GET'])
@login_required
def project(project_id):
    '''
    项目显示细节
    '''
    # print 'projects', current_user.projects
    color = ['info', 'info', 'info', 'warning', 'warning', 'danger']
    p = Project.query.get_or_404(project_id)
    finish_steps_length = Step.query.filter_by(project_id=p.id, status=1).count()
    steps_length = float(len(list(p.steps)))
    progress = finish_steps_length / steps_length * 100
    remained_days = p.expected_finish_at - datetime.now()
    other_users = db.session.query(User).filter(User.id.notin_([u.id for u in p.users])).all()
    # print [u.id for u in p.users], [u.id for u in other_users]
    if current_user.admin:
        projects = Project.query.order_by(Project.priority.desc()).all()
    else:
        projects = current_user.projects.order_by(Project.priority.desc()).all()
    return render_template('project.html', project=p, projects=projects,
                           progress=progress, finish_steps_length=finish_steps_length,
                           steps_length=steps_length, remained_days=remained_days,
                           other_users=other_users, commits=p.commits, color=color)


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
    record = Record(project=p, content=u'{0}完成了步骤{1}, 备注：{2}'.format(current_user.name, s.content, remark))
    db.session.add(record)
    finish_steps_length = float(Step.query.filter_by(project_id=p.id, status=1).count())
    for i in p.steps:
        if i.status == False:
            break
    else:
        p.status = True
        p.finish_at = datetime.now()
        db.session.add(p)
        p_status = 1
        record = Record(project=p, content=u'项目已完成')
        db.session.add(record)
    db.session.commit()
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
    priority = request.form.get('priority')
    steps = []
    for i in range(1, len(request.form) - 4):
        steps.append(request.form.get('step' + str(i)))
    p = Project(name=project_name, content=project_content, create_id=current_user.id,
                start_time=start_time, expected_finish_at=finish_time, priority=priority)
    db.session.add(p)
    db.session.commit()
    user = current_user._get_current_object()
    user.projects.append(p)
    db.session.add(user)
    for i in steps:
        s = Step(content=i, project=p)
        db.session.add(s)
    record = Record(project=p, content=u'{0}创建了此项目'.format(current_user.name))
    db.session.add(record)
    db.session.commit()
    flash(u'创建成功')
    return redirect(url_for('main.project', project_id=p.id))


@main.route('/project/<project_id>/addUser', methods=['POST'])
@login_required
def add_user(project_id):
    users_id = [r for r in request.form]
    p = Project.query.get_or_404(project_id)
    users = db.session.query(User).filter(User.id.in_(users_id)).all()
    for u in users:
        record = Record(project=p, content=u'{0}邀请{1}加入项目'.format(current_user.name, u.name))
        db.session.add(record)
        p.users.append(u)

    db.session.add(p)
    db.session.commit()
    flash(u'添加成功')
    return redirect(url_for('main.project', project_id=project_id))


@main.route('/project/step/<sid>/cancel')
@login_required
def step_status_cancel(sid):
    s = Step.query.get_or_404(sid)
    s.status = 0
    s.finish_remark = ''
    s.finish_at = None
    p = s.project
    db.session.add(s)
    record = Record(project=p, content=u'{0}将步骤{1}转为未完成'.format(current_user.name, s.content))
    db.session.add(record)
    if p.status == 1:
        p.status = 0
        p.finish_at = None
        db.session.add(p)
        record = Record(project=p, content=u'项目状态转为未完成'.format(current_user.name, s.content))
        db.session.add(record)
    db.session.commit()
    return redirect(url_for('.project', project_id=s.project.id))


@main.route('/project/<project_id>/removeUser', methods=['POST'])
@login_required
def remove_user(project_id):
    p = Project.query.get_or_404(project_id)
    users_id = [r for r in request.form]
    users = db.session.query(User).filter(User.id.in_(users_id)).all()
    for u in users:
        record = Record(project=p, content=u'{0}将{1}从项目中移除'.format(current_user.name, u.name))
        db.session.add(record)
        p.users.remove(u)
    db.session.add(p)
    db.session.commit()
    flash(u'移除成功')
    return redirect(url_for('main.project', project_id=project_id))


@main.route('/project/git/commit/<p_id>', methods=['POST'])
def git_commit(p_id):
    p = Project.query.get_or_404(p_id)
    data = json.loads(unicode(request.data))
    c = Commit(branch=data['branch'], ref=data['hashref'], cname=data['name'],
               cemail=data['email'], message=data['message'], project=p)
    db.session.add(c)
    record = Record(project=p, content=u'git账户{0}<{1}>提交了一次commit，备注是{2}'.format(data['name'],
                                                                                 data['email'], data['message']))
    db.session.add(record)
    db.session.commit()
    return 'ok', 200
