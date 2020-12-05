## 相关数据结构

### 用户
```json
User = {
    "id" = Interger,//自增的，每个用户是唯一的
    "username": string,  //不可重复的，每个用户是唯一的
    "email": string,    //以后改密码需要给邮箱发邮件，功能尚未实现
    "password": string, //使用加盐哈希加密
    "avater": string, //还没想好怎么存
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
    "email": "12345678" (string,邮箱名) ,
    "password": string
}

// 登录成功
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
		"profile": Userprofile
    }
}

// 在登录状态下登录其他账号
response.body = {
    "code": 400,
    "data": {
        "msg": "error"
    }
}

// 参数错误（缺少邮箱密码、用户不存在）：
response.body = {
    "code": 300,
    "data": {
        "msg": "wrong parameter"
    }
}

// 登陆失败：
response.body = {
    "code": 300,
    "data": {
        "msg": "email or password error"
    }
}
```

#### Logout 注销

POST /user/logout

``` json
request.body = { }

// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "success"
    }
}
```

#### UserProfile 查看个人信息

GET /user/profile

``` json
request.body = {
    "userID": number, // 可选参数，id为空则查看自己的个人信息
}

// 成功返回
response.body = {
    "code": 200,
    "data": {
        "msg": "success",
        "profile": Userprofile
    }
}

// 用户不存在
response.body = {
    "code": 300,
    "data": {
        "msg": "user does not exist",
        "profile": {}
    }
}
```

#### UserProfile_modify 修改个人信息

PUT /user/profile

``` json
request.body = { // 四项至少一个不为空
    "avatar": string,
    "username": string,
    "nickname":string,
    "motto":string
}

// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "success"
    }
}

// 用户名重复
response.body = {
    "code": 300,
    "data": {
        "msg": "duplicate username"
    }
}

// 四项均为空
response.body = {
    "code": 300,
    "data": {
        "msg": "parameter error"
    }
}

// 用户名重复
response.body = {
    "code": 300,
    "data": {
        "msg": "duplicate username"
    }
}

// 头像文件不存在
response.body = {
    "code": 300,
    "data": {
        "msg": "unexisted avatar"
    }
}

// 用户名重复且头像文件不存在
response.body = {
    "code": 300,
    "data": {
        "msg": "duplicate username/unexisted avatar"
    }
}
// 参数输入过长（超过100字符）
response.body = {
    "code": 300,
    "data": {
        "msg": "parameter too long"
    }
}
```
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
