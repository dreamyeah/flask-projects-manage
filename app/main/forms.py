# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required,Length


class ProjectForm(Form):
    content = StringField('', validators=[Required(),Length(1,200)])
    submit = SubmitField('Submit')
#
#
# class CircleForm(Form):
#     name = StringField('工作圈名字', validators=[Required(),Length(1,20)])
#     describe = StringField('描述(少于100字)', validators=[Required(),Length(1,100)])
#     submit = SubmitField('创建')
