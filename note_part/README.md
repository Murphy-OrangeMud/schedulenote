## APIs

#### 修改笔记

POST /modifyNotes

```json
request.body = {
    "ID" : String,
    "sourceCode" : String
}
若笔记存在：
response.body = {
    "state" : "OK"
}
若笔记不存在：
response.body = {
    "state" : "ERR"
}
```

#### 预览笔记

POST /previewNotes

```json
request.body = {
    "ID" : String
}
若笔记存在：
response.body = HTML
若笔记不存在：
response.body = {
    "state" : "ERR"
}
```

#### 导出PDF

POST /exportPDF

```json
request.body = {
    "ID" : String
}
若笔记存在：
response.body = File
若笔记不存在：
response.body = {
    "state" : "ERR"
}
```

#### 新建笔记

POST /newNote

```json
request.body = {
    "sourceCode" : String,
    "owner" : Integer,
    "course_belonged" : String
}
response.body = {
    "state": "OK"
}
```

#### 赞

POST /upVote

```json
request.body = {
    "ID" : String
}
若笔记存在：
response.body = {
    "state" : "OK"
}
若笔记不存在：
response.body = {
    "state" : "ERR"
}
```

#### 踩

POST /downVote

```json
request.body = {
    "ID" : String
}
若笔记存在：
response.body = {
    "state" : "OK"
}
若笔记不存在：
response.body = {
    "state" : "ERR"
}
```

#### 用ID得到笔记内容

POST /getNote

```json
request.body = {
    "ID" : String
}
若笔记存在：
response.body = {
    "sourceCode" : String,
    "owner" : Integer,
    "course_belonged" : String,
    "ups" : Integer,
    "createTime" : DateTime,
    "modifyTime" : DateTime
}
若笔记不存在：
response.body = {
    "state" : "ERR"
}
```

#### 得到所有笔记ID

GET /getAllNoteID

```json
response.body = IDList
```

