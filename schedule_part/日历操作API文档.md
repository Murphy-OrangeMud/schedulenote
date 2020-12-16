## 相关数据结构

#### 日程
``` json
{
    "ID": string,
    "discription": string, 
    "location": string, 
    "startTime": string("yyyy-mm-dd hh-mm-ss"), 
    "endTime": string("yyyy-mm-dd hh-mm-ss"), 
    "rotation": int,
    "userID": string,
    "type": scheduleType/int
}
```

## 相关操作

#### 用户操作

###### 获取日历

注：结合demo，getcalendar和getclasscalendar返回的“数组”按照起始时间排序，getdeadlinecalendar按照终止时间排序。

POST /getcalendar

POST /getclasscalendar

POST /getdeadlinescalendar

``` json
request.body = {
    "userID": string
}
response.body = {
    "status": "OK",
    "calendar": 
    [
        {
            "id": string,
            "discription": string, 
            "location": string, 
            "startTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
            "endTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
            "rotation": int,
            "userID": string,
            "type": scheduleType/int
        }, 
        {
            "id": string,
            "discription": string, 
            "location": string, 
            "startTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
            "endTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
            "rotation": int,
            "userID": string,
            "type": scheduleType/int
        },
        ...
    ]
}
```

###### 增加DDL

POST /addschedule
``` json
request.body = {
    "discription": string, 
    "location": string, 
    "startTime": string("yyyy-mm-dd hh:mm:ss"), 
    "endTime": string("yyyy-mm-dd hh:mm:ss"), 
    "rotation": int,
    "userID": string,
    "type": scheduleType/int
}
response.body = {
    "status": "OK"
}
```

###### 删除DDL

POST /deleteddl
``` json
request.body = {
    "ID": string,
}
response.body = {
    "status": "OK"
}
```

###### 修改DDL

POST /modifyschedule
``` json
request.body = {
    "id": string, //待修改的ddl的ID
    //以下为新参数，如果这一项不需要修改，则维持原值，或设置为空字符串，rotation设置成比-10小的很小的负数，type应该是不需要修改的。这样泛化过后的接口能够继续适应修改课程的操作而不仅仅是ddl（二者函数写法类似）
    "discription": string, 
    "location": string, 
    "startTime": string("yyyy-mm-dd hh-mm-ss"), 
    "endTime": string("yyyy-mm-dd hh-mm-ss"), 
    "rotation": int,
    "userID": string,
    "type": scheduleType/int
}
response.body = {
    "status": "OK"
}
```

###### 得到警告

GET /getalert
``` json
{
    "alertddl": {
        "id": string,
        "discription": string, 
        "location": string, 
        "startTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
        "endTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
        "rotation": int,
        "userID": string,
        "type": scheduleType/int
    }
}
```

