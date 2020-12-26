## 相关数据结构

### 用户
```json
User = {
    "id" = Interger,//自增的，每个用户是唯一的
    "username": string,  //不可重复的，每个用户是唯一的
    "email": string,    //以后改密码需要给邮箱发邮件，功能尚未实现
    "password": string, //使用加盐哈希加密
    "avatar": string, //还没想好怎么存
    "motto": string, //个性签名
    "is_admin":Integer // 0 or 1
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
一定要先验证email，然后才能注册

POST /user/signup
```json
request.body = {
    //长度均不超过64，也都不能为空，否则报参数错误
    "name":string,
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
        "email": email
    }
}

//参数为空或过长（超过64个字节）
response.body = {
    "code" : 700, 
    "data" : {
        "msg":"parameter ILLEGAL",
        "username":name,
        "email": email
    } 
}

//用户已存在
response.body = {
    "code" : 400, 
    "data" : {
        "msg":"User " + name + " already exits",
        "username":name,
        "email": email
    } 
}

//邮箱已被占用
response.body = {
    "code": 400,
    "data": {
        "msg": "The mailbox is already occupied",
        "username": name,
        "email": email
    }
}

//邮箱未验证
response.body = {
    "code": 400,
    "data": {
        "msg": "The mailbox was not verified",
        "username": name,
        "email": email
    }
}

//数据库出现错误
response.body = {
    "code" : 300, 
    "data" : {
        "msg":"Database error",
        "username":name,
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
        "name": string,
        "id" : number,
        "motto" : string,
        "avatar":{
            "code" : 200,
            "img_type" : ALLOWED_EXTENSIONS,
            "img_stream" : filestream
            //返回base64编码下的图片流
        },
        "is_admin":1 or 0
    }
}

// 在登录状态下登录其他账号
response.body = {
    "code": 400,
    "data": {
        "msg": "User %current_user.name is using now"
    }
}

// 参数非法
response.body = {
    "code": 900,
    "data": {
        "msg": "parameter ILLEGAL"
    }
}

//用户不存在
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
#### login_by_email
在此之前需要先查看拥有该邮箱的用户是否存在（search_email），然后完成邮箱验证（get_mail_verify, check_mail_verify），否则会登录失败

POST user/login_by_email
```json
request.body = {
    "email": "12345678@pku.edu.cn" (string邮箱名)
}

//登录成功
response.body = {
    "code": 200,
    "data": {
        "msg": "User  + username +  login success"
        "name": string,
        "id" : number,
        "motto" : string,
        "avatar":{
            "code" : 200,
            "img_type" : ALLOWED_EXTENSIONS,
            "img_stream" : filestream
            //返回base64编码下的图片流
        },
        "is_admin":1 or 0
    }
}

//用户不存在，如果完成了search_email则不会出这样的错误
response.body = {
    "code": 400,
    "data": {
        "msg": "User doesn\'t exist"
    }
}

//邮箱未验证
response.body = {
    "code": 400,
    "data": {
        "msg": "The mailbox was not verified",
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
        },
        "is_admin":1 or 0
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
    "newemail":string
}

// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "Something modify success" 
        //Something可以是Username, Password等修改项
    }
}

//邮箱未验证(只有修改邮箱时发生)
response.body = {
    "code": 400,
    "data": {
        "msg": "The mailbox was not verified",
    }
}

// 用户名重复（只有修改用户名时发生）
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
### 反馈管理
```json
Feedback = {
    id : Int,
    finished : Int, //0 or 1
    msg : string, 
    whistleBlower_id : Int
}

Report = {
    id : Int,
    finished : Int, //0 or 1
    //被举报者id
    reported_id: Int,
    //被举报类型，包括昵称、头像、座右铭、笔记文件四种，分别用0、1、2、3代表
    to_report:Int,
    msg : string, 
    file_id : string,
    whistleBlower_id : Int
}
```
#### 意见反馈
POST /user/feedback
```json
request.body = {  //第一项为个人信息（可不填）
    "msg":string, //关于反馈的内容
    "anonymous":0 or 1 //是否选择匿名
}

response.body{
    "code":200,
    "data":{
        "msg":"feedback success"
    }
}

// msg参数非法
response.body = {
    "code": 900,
    "data": {
        "msg": "message can not be None or Too long(over 200 bytes)"
    }
}

//数据库发生错误
response.body = {
    "code": 900,
    "data": {
        "msg": "Database error"
    }
}
```
#### 举报
POST /user/report
``` json
request.body = { 
    "msg":string, //关于举报的描述
    "reported_id":int,//被举报人id，必填
    "to_report":int,//举报内容，0,1,2,3分别代表 昵称、头像、座右铭、笔记文件
    "file_id":string,//文件号，如果to_report=3则必填
    "anonymous":0 or 1 //是否匿名
}

response.body = {
    "code":200,
    "data":{
        "msg":"report success"
    }
}

// 被举报者不存在
response.body = {
    "code": 400,
    "data": {
        "msg": "User does not exist"
    }
}

//举报内容为文件，文件号为空
response.body = {
    "code": 900,
    "data": {
        "msg": "Error: file_id empty"
    }
}

// msg参数非法
response.body = {
    "code": 900,
    "data": {
        "msg": "message can not be None or Too long(over 200 bytes)"
    }
}

//数据库发生错误
response.body = {
    "code": 300,
    "data": {
        "msg": "Database error"
    }
}

```
### 管理员部分
#### 获得未处理的反馈信息（feedback）
GET admin/feedback_list
```json
request.body = {}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "get unfinished feedback successfully",
        "id_list": [未处理的feedback id]
    }
}

//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}
```

#### 获得未处理的举报信息（report）
GET admin/feedback_list
```json
request.body = {}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "get unfinished report successfully",
        "id_list": [未处理的report id]
    }
}

//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}
```

#### 获得某一条反馈信息
GET admin/get_feedback/<id>
```json
request.body = {}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "feedback {id} get",
        "feedback" = Feedback详细信息
    }
}

//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}

//该条feedback不存在
response.body = {
    "code": 300,
    "data": {
        "msg": "feedback {id} not exist",
    }
}
```

#### 获得某一条举报信息
GET admin/get_report/<id>
```json
request.body = {}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "report {id} get",
        "report" = report详细信息
    }
}

//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}

//该条report不存在
response.body = {
    "code": 300,
    "data": {
        "msg": "report {id} not exist",
    }
}
```

#### 处理完成feedback
POST admin/finish_feedback/<id>
```json
request.body = {}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "feedback {id} finished",
    }
}

//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}

//该条feedback不存在或数据库错误
response.body = {
    "code": 300,
    "data": {
        "msg": "feedback {id} not exist or database error",
    }
}
```

#### 处理完成report
POST admin/finish_report/<id>
```json
request.body = {}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "report {id} finished",
    }
}

//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}

//该条report不存在或数据库错误
response.body = {
    "code": 300,
    "data": {
        "msg": "report {id} not exist or database error",
    }
}
```

#### 管理员修改用户信息
PUT admin/admin_modify
```json
request.body = {
    "report_type":int,
    "file_id":string
}

//成功
response.body = {
    "code": 200,
    "data": {
        "msg": "Modify reported_user {name}'s {re_type} to \"{new_one}\""
    }
}
//非管理员操作
response.body = {
    "code": 400,
    "data": {
        "msg": "You are not an administrator",
    }
}

//文件不存在或数据库错误
response.body = {
    "code": 300,
    "data": {
        "msg": "file id {id} error or database error",
    }
}

//参数无法识别
response.body = {
    "code": 900,
    "data": {
        "msg": "Modify type undefined",
    }
}
```