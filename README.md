#基于Flask的项目管理网站 

##基于Flask的项目管理网站
开发：Flask + MySql
部署：gunicorn + nginx + supervisor + 阿里云 ubuntu 14.04 
###基本功能：
* 用户登录注册
* 项目新建、提交、进度，管理等
* 总体统计信息
* 项目树关系图
* 文件中转
###模型
USER

```
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40))
    passwd = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=0)
    image_url = db.Column(db.String(500))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project',
                               secondary=registrations,
                               backref=db.backref('users', lazy='dynamic'),
                               lazy='dynamic')
    create_projects = db.relationship('Project',
                                      foreign_keys=[Project.create_id],
                                      backref=db.backref('creator', lazy='joined'),
                                      lazy='dynamic',
                                      cascade='all, delete-orphan')
```
PROJECT
```
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    content = db.Column(db.Text)
    status = db.Column(db.Boolean, default=0)
    start_time = db.Column(db.DateTime)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    expected_finish_at = db.Column(db.DateTime)
    finish_at = db.Column(db.DateTime, nullable=True)
    create_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    steps = db.relationship('Step', backref='project', lazy='dynamic')
    commits = db.relationship('Commit', backref='project', lazy='dynamic')
    priority = db.Column(db.Integer, default=0)
    records = db.relationship('Record', backref='project', lazy='dynamic')
    del_flag = db.Column(db.Boolean, default=False)
    father_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    father = db.relationship('Project', backref='children', remote_side=[id])
    git_name = db.Column(db.String(40), nullable=True)
```
STEP
```
    id = db.Column(db.String(50), primary_key=True, default=next_id, unique=True)
    content = db.Column(db.Text)
    status = db.Column(db.Boolean, default=0)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    finish_at = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    finish_remark = db.Column(db.Text, nullable=True)
    del_flag = db.Column(db.Boolean, default=False)
```
COMMIT
```
    id = db.Column(db.String(50), primary_key=True, default=next_id, unique=True)
    branch = db.Column(db.String(80))
    ref = db.Column(db.String(40))
    cname = db.Column(db.String(50))
    cemail = db.Column(db.String(50))
    message = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
```
RECORD
```
    id = db.Column(db.String(50), primary_key=True, default=next_id, unique=True)
    branch = db.Column(db.String(80))
    ref = db.Column(db.String(40))
    cname = db.Column(db.String(50))
    cemail = db.Column(db.String(50))
    message = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
```

####暂未解决的问题☑ 
* 邀请成员加入功能--已经解决 ☑2016/8/10
* 如何与git服务器交互，同步git上的commit数据--已解决2016/8/10☑
* 历史项目 已解决☑
* 完成备注 已解决☑
* 管理part 已解决☑
* 项目树形图  已解决☑
* 统计信息 已解决☑
* 文件分享 已解决☑

##页面截图
* 首页
![登录](http://o6gcipdzi.bkt.clouddn.com/%E7%99%BB%E5%BD%95.png)
* 注册
![注册](http://o6gcipdzi.bkt.clouddn.com/%E6%B3%A8%E5%86%8C.png)
* 首页
![首页](http://o6gcipdzi.bkt.clouddn.com/%E9%A6%96%E9%A1%B5.png)
* 管理
![管理](http://o6gcipdzi.bkt.clouddn.com/%E7%AE%A1%E7%90%86.png)
* 新建
![新建](http://o6gcipdzi.bkt.clouddn.com/%E6%96%B0%E5%BB%BA.png)
* 编辑
![编辑](http://o6gcipdzi.bkt.clouddn.com/%E7%BC%96%E8%BE%91.png)
* 项目树
![项目树](http://o6gcipdzi.bkt.clouddn.com/%E9%A1%B9%E7%9B%AE%E6%A0%91.png)
* 统计
![统计](http://o6gcipdzi.bkt.clouddn.com/%E7%BB%9F%E8%AE%A1.png)
* 统计
![文件中转](http://o6gcipdzi.bkt.clouddn.com/%E6%96%87%E4%BB%B6%E4%B8%AD%E8%BD%AC.png)