## 课程操作

### 数据结构

#### 用户

```json
User = {
    "name": string,
    "userID": number,
}
```

#### 课程资料

```json
File = {
    "description": String,
    "filename":String,
    "file":file,
    "Score":Real,
    "uploader":User
}
```



## Codes

```json
CODE = {
    "success": 200,
    "database_error": 300,
    "user_error": 400,
    "method_error": 600,
    "parameter_error": 700,
}
```

## APIs

### 上传课程资料

POST /course/upload

```json
request.body={
    "uploader": int, // id
    "course" : int, // courseid
    "description" : str,
    "file": File
}
//成功
response.body = {
    "code": 200,
}
//文件重复
response.body = {
    "code": 400,
}
```

### 删除文件

DELETE /course?id=123

```json
// 成功
response.body = {
    "code": 200,
    "data": {
        "msg": "delete post successfully"
    }
}
```

### 获得文件

GET /course/download

```json
// 成功
response.body = {
    "code": 200,
    "data": {
        "file": File
    }
}
```

### 赞文件

POST /course/upvote

```json
request.body = {
    "id": number
}
```

### 踩文件

POST /course/downvote

```json
request.body = {
    "id": number
}
```