# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for , current_app
from flask.ext.login import login_required, current_user
from ..models import Project, User
from . import manage
from .. import db


@manage.route("/", methods=['GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.projects.filter_by(del_flag=False).order_by(Project.create_at.desc()).paginate(
        page, per_page=current_app.config['TASK_POSTS_PER_PAGE'],
        error_out=False)
    return render_template('manage/manage_project.html', projects=pagination.items, pagination=pagination)


@manage.route("/all", methods=['GET'])
@login_required
def all_projects():
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.filter(Project.creator != current_user).filter_by(
        del_flag=False).order_by(Project.create_at.desc()).paginate(
        page, per_page=current_app.config['TASK_POSTS_PER_PAGE'],
        error_out=False)
    other_users = User.query.all()
    return render_template('manage/manage_all.html', projects=pagination.items, pagination=pagination,
                           other_users=other_users)


@manage.route("/dustbin", methods=['GET'])
@login_required
def dustbin():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.projects.filter_by(del_flag=True).order_by(Project.create_at.desc()).paginate(
        page, per_page=current_app.config['TASK_POSTS_PER_PAGE'],
        error_out=False)
    other_users = User.query.all()
    return render_template('manage/manage_dustbin.html', projects=pagination.items, pagination=pagination,
                           other_users=other_users)


@manage.route("/delete/<project_id>", methods=['PUT'])
@login_required
def delete_project(project_id):
    p = Project.query.get_or_404(project_id)
    p.del_flag = True
    # for s in p.steps:
    #     db.session.delete(s)
    db.session.add(p)
    db.session.commit()
    return 'ok', 200


@manage.route("/quit/<project_id>", methods=['PUT'])
@login_required
def quit_project(project_id):
    u = current_user._get_current_object()
    p = Project.query.get_or_404(project_id)
    p.users.remove(u)
    db.session.add(p)
    db.session.commit()
    return 'ok', 200


@manage.route("/filter/minus/<info>", methods=['GET'])
@login_required
def filter_minus(info):
    user_ids = info.strip('&').split('&')
    users = User.query.filter(User.id.in_(user_ids)).all()
    if len(users) > 0:
        minus_projects=set(users[0].projects)
        for i in xrange(1,len(users)):
            minus_projects = set(users[i].projects) & minus_projects

    else:
        minus_projects = {}
    # diff_projects = list(set(all_projects))
    # for p in diff_projects:
    #     all_projects.remove(p)
    other_users = User.query.all()

    return render_template('manage/filter_minus.html', projects=minus_projects,
                           other_users=other_users)


@manage.route("/filter/union/<info>", methods=['GET'])
@login_required
def filter_union(info):
    user_ids = info.strip('&').split('&')
    users = User.query.filter(User.id.in_(user_ids)).all()
    other_users = User.query.all()
    return render_template('manage/filter_union.html', users=users,
                           other_users=other_users)


@manage.route("/recover/<project_id>", methods=['PUT'])
@login_required
def recover_project(project_id):
    p = Project.query.get_or_404(project_id)
    p.del_flag = False
    db.session.add(p)
    db.session.commit()
    return 'ok', 200


@manage.route("/indeed_delete/<project_id>", methods=['DELETE'])
@login_required
def indeed_delete_project(project_id):
    p = Project.query.get_or_404(project_id)
    for s in p.steps:
        db.session.delete(s)
    db.session.delete(p)
    db.session.commit()
    return 'ok', 200
