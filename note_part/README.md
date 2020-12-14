## APIs

#### 修改笔记

POST /modifyNotes

```json
request.body = {
    "ID" : String,
    "sourceCode" : String
}
response.body = {
    "state" : "OK"
}
```

#### 预览笔记

POST /previewNotes

```json
request.body = {
    "ID" : String
}
response.body = HTML
```

#### 导出PDF

POST /exportPDF

```json
request.body = {
    "ID" : String
}
response.body = File
```

#### 新建笔记

POST /newNote

```json
request.body = {
    "sourceCode" : String,
    "owner" : String,
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
response.body = {
    "state" : "OK"
}
```

#### 踩

POST /downVote

```json
request.body = {
    "ID" : String
}
response.body={
    "state": "OK",
}
```

#### 用ID得到笔记内容

POST /getNote

```json
request.body = {
    "ID" : String
}
response.body = {
    "sourceCode" : String,
    "owner" : String,
    "course_belonged" : String,
    "ups" : Integer,
    "createTime" : DateTime,
    "modifyTime" : DateTime
}
```

#### 得到所有笔记ID

GET /getAllNoteID

```json
response.body = IDList
```
