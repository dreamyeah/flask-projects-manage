# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from ..models import Project
from . import manage
from .. import db


@manage.route("/", methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.projects.order_by(Project.create_at.desc()).paginate(
        page, per_page=current_app.config['TASK_POSTS_PER_PAGE'],
        error_out=False)
    return render_template('manage/manage_project.html',projects=pagination.items,
                           pagination=pagination)


@manage.route("/delete/<project_id>", methods=['DELETE'])
@login_required
def delete_project(project_id):
    p = Project.query.get_or_404(project_id)
    for s in p.steps:
        db.session.delete(s)
    db.session.delete(p)
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



