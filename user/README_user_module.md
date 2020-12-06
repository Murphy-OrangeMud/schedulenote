# User Module 开发说明
本文档持续更新中
## 基本User结构
详见User.py，User继承了UserMixin和db.Model，这使得User类既可以使用flask_login提供的方法（如LoginManager ，logout_user，login_required，current_user），也可以作为SQLAlchemy.Model来调用一些数据库相关的函数。

目前只制作了基础版本，User的属性有：
```
"id" = Interger,//自增的，每个用户是唯一的
"username": string,  //不可重复的，每个用户是唯一的
"email": string,    //以后改密码需要给邮箱发邮件，功能尚未实现
"password": string, //使用加盐哈希加密
"avater": string, //还没想好怎么存
"motto": string //个性签名
```

提供了一些api，目前完成的有signup，login，logout，以经过一系列测试，可以正常使用。详细内容请察看api_doc

## 提供给其他模块开发者的内容
flask_login提供了一些大家都可以使用的内容，方便大家开发。大家需要从flask_login import xx，例如`from flask_login import login_required, current_user`
### @login_required
该函数修饰器会保证某函数只有在用户登录后才可以访问，用户未登录强行访问，会自动重定向到登录页面（如果没有设置登录页面，则会返回401错误）。使用方法如下
```python
@app.route('/somewhere', methods = ['GET', 'POST'])
@login_required
def fun():
    # do something
    return something
```
如果用户没有登录，则无法访问该路径

### current_user
如果用户未登录，则current_user为一个AnonymousUserMixin类，若用户已登录，则current_user为已登陆User对象，可以用访问User对象的方法直接访问。例如
```python
print(current_user.id)
print(current_user.username)
```