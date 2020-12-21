## 相关数据结构

### 用户
```json
User = {
    "id" = Interger,//自增的，每个用户是唯一的
    "username": string,  //不可重复的，每个用户是唯一的
    "email": string,    //以后改密码需要给邮箱发邮件，功能尚未实现
    "password": string, //使用加盐哈希加密
    "avatar": string, //还没想好怎么存
    "motto": string //个性签名
}
这里可以把课表信息、课程信息、笔记信息加入进来，待完善
```



## APIs
```
CODE = {
    "success": 200,
    "database_error": 300,
    "user_error": 400,
    "method_error": 600,
    "parameter_error": 700,
}
```

### 邮件验证相关
使用smtplib实现了SSL加密的邮件功能，以下是一些会用到的api

#### search_email
用于在login_by_email前，确认该邮箱是否存在于用户数据中

GET /user/search_email
```json
request.body = {
    "email": "12345678@pku.edu.cn" (string邮箱名)
}

//用户存在
response.body = {
    "code": 200,
    "data": {
        "msg": "success"
    }
}

//用户不存在
response.body = {
    "code": 400,
    "data": {
        "msg": "User not exist"
    }
}
```
#### get_mail_verify
获取邮件验证码，验证码会以<email, verify_code>的形式存在Redis中，持续5min。在signup, login_by_email和modify email三个场景可能用到

GET user/get_mail_verify
```json
request.body = {
    "email": "12345678@pku.edu.cn" (string邮箱名)
}

//发送成功
response.body = {
    "code": 200,
    "data": {
        "msg": "Get verify code successfully"
    }
}

//发送失败
response.body = {
    "code": 900,
    "data": {
        "msg": "Email can't use or Network congestion"
    }
}
```

#### check_mail_verify
用于确认验证码，如果验证码正确，则将<email, verify_code>删除，再将<email_checked, email>存入Redis。signup, login_by_email和modify email三个场景可以通过检查<email_checked, email>来确认验证码，持续5min

POST user/check_mail_verify
```json
request.body = {
    "email": "12345678@pku.edu.cn" (string邮箱名),
    "verify_code": string
}
//验证码正确
response.body = {
    "code": 200,
    "data": {
        "msg": "Check verify code successfully"
    }
}
//验证码错误
response.body = {
    "code": 900,
    "data": {
        "msg": "Verify code error"
    }
}
//验证码不存在或已经过期
response.body = {
    "code": 900,
    "data": {
        "msg": "The verification code does not exist or has expired"
    }
}
```

### 用户相关

#### Signup 注册
POST /user/signup
```json
request.body = {
    //长度均不超过64，也都不能为空，否则报参数错误
    "username":string,
    "password": string,
    "email": "12345678@pku.edu.cn" (string,邮箱名)
}

// 注册成功
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
        "id": id
		"username":name,
        "password": password, 
        "email": email
    }
}

//参数为空或过长（超过64个字节）
response.body = {
    "code" : 700, 
    "data" : {
        "msg":"parameter ILLEGAL",
        "username":name,
        "password": password, 
        "email": email
    } 
}

//用户已存在
response.body = {
    "code" : 400, 
    "data" : {
        "msg":"User " + name + " already exits",
        "username":name,
        "password": password, 
        "email": email
    } 
}

//数据库出现错误
response.body = {
    "code" : 300, 
    "data" : {
        "msg":"Database error",
        "username":name,
        "password": password, 
        "email": email
    } 
}
                
```

#### Login 登陆

POST /user/login

``` json
request.body = {
    "name": string,
    "password": string
}

// 登录成功
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
		"profile": Userprofile //这里代指除password以外的全部用户信息，目前只有id, username, email, avatar, motto
    }
}

// 在登录状态下登录其他账号
response.body = {
    "code": 400,
    "data": {
        "msg": "User %current_user.name is using now"
    }
}

// 参数非法或用户不存在：
response.body = {
    "code": 400,
    "data": {
        "msg": "User  "%name"  doesn't exist"
    }
}

// 密码错误：
response.body = {
    "code": 300,
    "data": {
        "msg": "Password to  User "%name" is error"
    }
}
```

#### Logout 登出

POST /user/logout

``` json
request.body = { }

// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "Logout Success"
    }
}
```

#### getuser 查看个人信息

GET /user/getuser

``` json
request.body = {
    //二者都空则查看自己的信息，二者都非空则以id为准
    "id": number,
    "name": string
}

// 成功返回, 头像也正常返回, avatar的code为200
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
        "is_current": 1 or 0, //如果是1，表示访问的是当前登录者的信息，如果是0，则不是当前登录者的信息
        "name": string,
        "id" : number,
        "motto" : string,
        "avatar":{
            "code" : 200,
            "img_type" : ALLOWED_EXTENSIONS,
            "img_stream" : filestream
            //返回base64编码下的图片流
        }
    }
}
// 成功返回, 头像从未初始化过，为None, avatar的code为400
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
        "is_current": 1 or 0, //如果是1，表示访问的是当前登录者的信息，如果是0，则不是当前登录者的信息
        "name": string,
        "id" : number,
        "motto" : string,
        "avatar":{
            "code" : 400,
            "msg" : "unexisted avatar"
        }
    }
}

// 成功返回,  头像无法读取（可能图片文件损坏或丢失），avatar的code为300
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
        "is_current": 1 or 0, //如果是1，表示访问的是当前登录者的信息，如果是0，则不是当前登录者的信息
        "name": string,
        "id" : number,
        "motto" : string,
        "avatar":{
            "code" : 300,
            "msg" : "avatar damaged"
            //返回base64编码下的图片流
        }
    }
}
// 用户不存在或参数错误
response.body = {
    "code": 400,
    "data": {
        "msg": "user can't be visited or parameter ILLEGAL",
    }
}
```



#### modify 修改个人信息

PUT /user/modify

``` json
request.body = { 
    // 每次只能更改一项，不可全空。多个有效参数，则只处理第一个有效参数。
    // 如newname和newpassword都符合要求，则只处理newname
    "newname": string,
    "newpassword":string,
    "newmotto":string,
}

// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "Something modify success" 
        //Something可以是Username, Password等修改项
    }
}

// 用户名重复
response.body = {
    "code": 400,
    "data": {
        "msg": "User \"%newname\" already exists"
    }
}

// 参数不合法
response.body = {
    "code": 900,
    "data": {
        "msg": "parameter ILLEGAL"
    }
}
``` 

#### upload_avatar
PUT /user/upload_avatar
```json
request.body = { 
    "avatar": file
}

// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "success" 
    }
}

//图片非jpg,jepg,png格式，或后缀名错误
response.body = {
    "code": 900,
    "data": {
        "msg": "abnormal image type" 
    }
}

```
# 后面的仅供参考，暂时未完成
### 反馈管理
#### 意见反馈
POST /supervision/feedback
```json
request.body = {  //第一项为个人信息（可不填）
    "user":USER,
    "msg":string //关于反馈的内容
}

response.body{
    "code":200,
    "data":{
        "msg":"success"
    }
}

// 参数输入过长（超过1000字符）
response.body = {
    "code": 300,
    "data": {
        "msg": "parameter too long"
    }
}
```
#### 举报其他用户
POST /supervision/report
``` json
request.body = { 
    "whistleblower":USER,//举报人信息，可不填
    "reported":USER,//被举报人信息，必填
    //举报内容，至少填一项
    "avatar": string,
    "username": string,
    "nickname":string,
    "motto":string,

    "msg":string //关于举报的描述
}

response.body{
    "code":200,
    "data":{
        "msg":"success"
    }
}

// 用户不存在
response.body = {
    "code": 300,
    "data": {
        "msg": "user does not exist"
    }
}

// 举报内容不全
response.body = {
    "code": 300,
    "data": {
        "msg": "parameter error"
    }
}
```
