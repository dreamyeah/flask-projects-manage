# -*- coding: utf-8 -*-
from flask import render_template, Markup, redirect, send_from_directory, abort, url_for,request,current_app
from flask.ext.login import login_required
from . import doc
import os
from manager import app
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc'])


def getdirsize(dir):
   size = 0L
   for root, dirs, files in os.walk(dir):
      size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size/1024


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@doc.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            print file.filename
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('doc.index'))
    all_things = os.listdir(current_app.config['UPLOAD_FOLDER'])
    files = filter(lambda x: os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], x)), all_things)
    # files = map(lambda x: x.decode('utf-8'), files)
    dirs = list(set(all_things) - set(files))
    dirs = filter(lambda x: not x.startswith('.'), dirs)
    sizes = {}
    for f in files:
        sizes[f] = os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], f))
    for d in dirs:
        sizes[d] = getdirsize(os.path.join(app.config['UPLOAD_FOLDER'], d))
    return render_template('doc/show_path.html', dirs=dirs, files=files, base_path=app.config['UPLOAD_FOLDER'],
                           sizes=sizes)


@doc.route('/show_dir/<basepath>/<dirpath>',methods=['GET', 'POST'])
@login_required
def show_dir(basepath, dirpath):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            print os.path.join(unicode(basepath), unicode(dirpath), file.filename)
            file.save(os.path.join(basepath, dirpath, file.filename))
        return redirect(url_for('doc.show_dir', basepath=basepath, dirpath=dirpath))
    if not basepath.startswith(app.config['UPLOAD_FOLDER']):
        abort(404)
    path = os.path.join(basepath, dirpath)
    all_things = os.listdir(path)
    files = filter(lambda x: os.path.isfile(os.path.join(path, x)), all_things)
    dirs = list(set(all_things) - set(files))
    dirs = filter(lambda x: x.startswith('.'), dirs)
    sizes = {}
    for f in files:
        sizes[f] = os.path.getsize(os.path.join(path, f))
    for d in dirs:
        sizes[d] = getdirsize(os.path.join(path, d))
    return render_template('doc/dir_show.html', dirs=dirs, files=files, base_path=path, sizes=sizes)



@doc.route('/show_doc/<basepath>/<filename>')
@login_required
def show_doc(basepath, filename):
    # path = os.path.join(basepath, filename)
    print basepath, filename
    return send_from_directory(basepath, filename)


@doc.route('/create_folder/<basepath>', methods=['POST'])
@login_required
def create_folder(basepath):
    filename = request.form.get('name')
    os.mkdir(os.path.join(basepath, filename))
    return redirect(url_for('doc.show_dir', basepath=basepath, dirpath=filename))

@doc.route('/downloads/<basepath>/<filename>')
def download_file(basepath, filename):
    return send_from_directory(basepath, filename, as_attachment=True)
