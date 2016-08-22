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
        p = Project.query.filter_by(del_flag=False).order_by(Project.priority.desc()).all()
    else:
        p = current_user.projects.filter_by(del_flag=False).order_by(Project.priority.desc()).all()
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
        all_projects = Project.query.all()
        remained_days = p[0].expected_finish_at - datetime.now()
        other_users = db.session.query(User).filter(User.id.notin_([u.id for u in p[0].users])).all()
        return render_template('project.html', project=p[0], projects=p, all_projects=all_projects,
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
    all_projects = Project.query.all()
    if current_user.admin:
        projects = Project.query.filter_by(del_flag=False).order_by(Project.priority.desc()).all()
    else:
        projects = current_user.projects.filter_by(del_flag=False).order_by(Project.priority.desc()).all()
    return render_template('project.html', project=p, projects=projects, progress=progress,
                           all_projects=all_projects, finish_steps_length=finish_steps_length,
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
    print request.form
    project_name = request.form.get('name')
    project_content = request.form.get('content')
    time = request.form.get('start_time')
    start_time = datetime.strptime(time, '%m/%d/%Y')
    time = request.form.get('finish_time')
    finish_time = datetime.strptime(time, '%m/%d/%Y')
    priority = int(request.form.get('priority'))
    steps = []
    for i in range(1, len(request.form) - 5):
        steps.append(request.form.get('step' + str(i)))
    if request.form.get('father') != u'None':
        father = Project.query.get_or_404(request.form.get('father'))
        p = Project(name=project_name, content=project_content, create_id=current_user.id,
                    father=father,start_time=start_time, expected_finish_at=finish_time,
                    priority=priority)
    else:
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
@login_required
def git_commit(p_id):
    p = Project.query.get_or_404(p_id)
    data = json.loads(unicode(request.data))
    c = Commit(branch=data['branch'], ref=data['hashref'], cname=data['name'],
               cemail=data['email'], message=data['message'], project=p)
    db.session.add(c)
    record = Record(project=p, content=u"git账户{0}<{1}>提交了一次commit，备注是:\"{2}\"".format(data['name'],
                                                                                    data['email'], data['message']))
    db.session.add(record)
    db.session.commit()
    return 'ok', 200


@main.route('/edit/<project_id>', methods=['GET'])
@login_required
def edit(project_id):
    p = Project.query.get_or_404(project_id)
    all_projects = Project.query.all()
    return render_template('edit.html', project=p, all_projects=all_projects, length=len(p.steps.all()))


@main.route('/edit_name/<project_id>', methods=['POST'])
@login_required
def edit_name(project_id):
    p = Project.query.get_or_404(project_id)
    old_name = p.name
    name = request.form.get('name')
    p.name = name
    db.session.add(p)
    record = Record(project=p, content=u"{0}将对项目名称进行了编辑，"
                                       u"从\"{1}\"更改为\"{2}\"".format(current_user.name, old_name, name))
    db.session.add(record)
    db.session.commit()
    return name, 200


@main.route('/edit_content/<project_id>', methods=['POST'])
def edit_content(project_id):
    p = Project.query.get_or_404(project_id)
    old_content = p.content
    content = request.form.get('content')
    p.content = old_content
    db.session.add(p)
    record = Record(project=p, content=u"{0}将对项目内容进行了编辑，"
                                       u"从\"{1}\"更改为\"{2}\"".format(current_user.name, old_content, content))
    db.session.add(record)
    db.session.commit()
    return content, 200


@main.route('/edit_start_time/<project_id>', methods=['POST'])
def edit_start_time(project_id):
    p = Project.query.get_or_404(project_id)
    old_time = p.start_time
    time = request.form.get('time')
    try:
        start_time = datetime.strptime(time, '%m/%d/%Y')
    except:
        return str(p.start_time), 200
    p.start_time = start_time
    db.session.add(p)
    record = Record(project=p, content=u"{0}将对项目开始时间进行了编辑，"
                                       u"时间从\"{1}\"更改为\"{2}\"".format(current_user.name, old_time, start_time))
    db.session.add(record)
    db.session.commit()
    return str(start_time), 200


@main.route('/edit_end_time/<project_id>', methods=['POST'])
def edit_end_time(project_id):
    p = Project.query.get_or_404(project_id)
    old_time = p.expected_finish_at
    time = request.form.get('time')
    try:
        end_time = datetime.strptime(time, '%m/%d/%Y')
    except:
        return str(p.expected_finish_at), 200
    p.expected_finish_at = end_time
    db.session.add(p)
    record = Record(project=p, content=u"{0}将对期望完成时间进行了编辑，"
                                       u"时间从\"{1}\"更改为\"{2}\"".format(current_user.name, old_time, end_time))
    db.session.add(record)
    db.session.commit()
    return str(end_time), 200


@main.route('/edit_priority/<project_id>', methods=['POST'])
def edit_priority(project_id):
    p = Project.query.get_or_404(project_id)
    old_priority = p.priority
    priority = int(request.form.get('priority'))
    p.priority = priority
    db.session.add(p)
    record = Record(project=p, content=u"{0}将对优先级进行了编辑，"
                                       u"优先级从\"{1}\"更改为\"{2}\"".format(current_user.name, old_priority, priority))
    db.session.add(record)
    db.session.commit()
    ret = ''

    for _ in range(priority):
        ret += '<span class ="glyphicon glyphicon-star" style="color: #f1c40f;" > </span>'
    return ret, 200


@main.route('/edit_step/<step_id>', methods=['POST'])
def edit_step(step_id):
    s = Step.query.get_or_404(step_id)
    old_content = s.content
    content = request.form.get('content')
    s.content = content
    db.session.add(s)
    record = Record(project=s.project, content=u"{0}将对步骤进行了编辑，"
                                               u"将\"{1}\"更改为\"{2}\"".format(current_user.name, old_content, s.content))
    db.session.add(record)
    db.session.commit()
    return content, 200


@main.route('/add_step/<project_id>', methods=['POST'])
def add_step(project_id):
    p = Project.query.get_or_404(project_id)
    s = Step(content=request.form.get('content'))
    db.session.add(s)
    p.steps.append(s)
    length = str(len(p.steps.all()))
    db.session.add(p)
    record = Record(project=p, content=u"{0}将添加了步骤\"{1}\"".format(current_user.name, s.content))
    db.session.add(record)
    db.session.commit()
    ret = u' <div class="form-group" id="step'+length+u'"><label for="inputStep1">步骤'+length+\
          u'</label><p><input type="text" style="display: inline;width: 93%" ' \
          u'class="form-control" id="'+s.id+u'"  ' \
          u'value="'+s.content+'" ><a style="display: inline" class="btn btn-danger"' \
          u'id="/step_remove/'+s.id+u'" >—</a></p></div>'
    return ret, 200


@main.route('/step_remove/<step_id>', methods=['GET'])
def remove_step(step_id):
    s = Step.query.get_or_404(step_id)
    p = s.project
    p.steps.remove(s)
    db.session.add(p)
    s.del_flag = True
    db.session.add(s)
    record = Record(project=p, content=u"{0}将删除了步骤\"{1}\"".format(current_user.name, s.content))
    db.session.add(record)
    db.session.commit()
    return '', 200


@main.route('/change_father_project/<project_id>', methods=['POST'])
def edit_father(project_id):
    father_id = request.form.get('father_id')
    p = Project.query.get_or_404(project_id)
    if father_id == 'None':
        p.father = None
        ret = 'None'
    else:
        f = Project.query.get_or_404(father_id)
        p.father = f
        ret = f.name
    db.session.add(p)
    record = Record(project=p, content=u"{0}将父项目转为\"{1}\"".format(current_user.name, ret))
    db.session.add(record)
    db.session.commit()
    return ret, 200


