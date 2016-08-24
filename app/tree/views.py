# -*- coding: utf-8 -*-
from flask import render_template, Markup
from flask.ext.login import login_required
from ..models import Project
from . import tree


def show_children(father, ret):
    if len(father.children) <= 0:
        ret += u'<li><span><i class="icon-sign"></i>' + father.name + u'</span><a href="/project/'+unicode(father.id)\
               + u'"> Goto </a></li>'
    else:
        ret += u'<li>'
        ret += u'<span><i class="icon-minus-sign"></i>' + father.name + u'</span><a href="/project/'+unicode(father.id)\
               + u'"> Goto </a>'
        ret += u'<ul>'
        for c in father.children:
            ret = show_children(c, ret)
        ret += u'</ul>'
        ret += u'</li>'
    return ret


@tree.route('/', methods=['GET'])
@login_required
def index():
    ps = Project.query.filter_by(father_id=None).all()
    print ps
    all_ret = ''
    for p in ps:
        ret = u'<ul>'
        ret = show_children(p, ret)
        ret += u'</ul>'
        all_ret += ret
    return render_template('tree/tree.html', ret=Markup(all_ret))


@tree.route('/<project_id>', methods=['GET'])
@login_required
def get_tree(project_id):
    p = Project.query.get_or_404(project_id)
    while p.father is not None:
        p = p.father
    ret = u'<ul>'
    ret = show_children(p, ret)
    ret += u'</ul>'
    return ret, 200


# @main.route('/get_all_tree', methods=['GET'])
# def get_all_tree():
#     ps = Project.query.filter_by(father_id=None).all()
#     print ps
#     all_ret = ''
#     for p in ps:
#         ret = u'<ul>'
#         ret = show_children(p, ret)
#         ret += u'</ul>'
#         all_ret += ret
#     return all_ret