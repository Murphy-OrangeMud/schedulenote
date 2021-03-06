# User Module 开发说明
## 基本User结构
详见User.py，User继承了UserMixin和db.Model，这使得User类既可以使用flask_login提供的方法（如LoginManager ，logout_user，login_required，current_user），也可以作为SQLAlchemy.Model来调用一些数据库相关的函数。

目前只制作了基础版本，User的属性有：
```
"id" = Interger,//自增的，每个用户是唯一的
"username": string,  //不可重复的，每个用户是唯一的
"email": string,    //用于完成邮件验证，不可重复
"password": string, //使用加盐哈希加密
"avater": string, //保存头像在服务器中存储的地址
"motto": string //个性签名
"is_admin": 0 或 1 //代表该用户是否为管理员
```

提供了一些api，详细内容请查看api_doc

## 提供给其他模块开发者的内容
flask_login提供了一些大家都可以使用的内容，方便大家开发。大家需要从flask_login import xx，例如`from flask_login import login_required, current_user`
### @login_required
该函数修饰器会保证某函数只有在用户登录后才可以访问，用户未登录强行访问，会返回401错误。使用方法如下
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
