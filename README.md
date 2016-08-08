# 基于Flask的项目管理网站


----------


## 注意
   还未完工.....





## 介绍
   此项目利用了python的微框架Flask，目前使用关系型数据库SQLite出储存项目信息。
####基本功能：
* 用户登录注册
* 项目新建、提交、进度


##模型
* USER
| 列名          | 类型          | 说明     |
| ------------- |:-------------:| -----:   |
| id            | Interger      |  工号    |
| name          | String(40)    | 用户名   |
| passwd        | String(128)   |  密码    |
| admin         | Boolean       | 管理权限 |
| image_url     | String(500)   |   头像   |
| create_at     | DateTime      | 创建时间 |
| projects      | relationship  | 指向PROJECT |

* PROJECT
| 列名          | 类型          | 说明         |
| ------------- |:-------------:| ------------:|
| id            | String(50)      |  项目ID    |
| name          | String(40)    | 项目名       |
| content       | Text          |  项目简介    |
| status        | Boolean       | 状态         |
| create_at     | String(500)   |   创建时间   |
| finish_at     | DateTime      | 完成时间     |
| create_id     | Interger      | 创建人 指向USER |
| steps         | relationship  | 步骤 指向STEP |


* STEP
| 列名          | 类型          | 说明       |
| ------------- |:-------------:| -----:     |
| id            | String(50)    |  步骤ID    |
| content       | Text          |  步骤简介  |
| status        | Boolean       | 状态       |
| create_at     | String(500)   | 创建时间   |
| finish_at     | DateTime      | 完成时间   |
| project_id    | Interger      | 所属项目 指向PROJECT |





### 暂未解决的问题
   如何与git服务器交互，同步git上的commit数据





