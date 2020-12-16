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
    //只需要填写需要修改的项。比如如果location不需要填写，就不需要location这个键值对
    "discription": string, 
    "location": string, 
    "startTime": string("yyyy-mm-dd hh-mm-ss"), 
    "endTime": string("yyyy-mm-dd hh-mm-ss"), 
    "rotation": int,
    "userID": string,
    "type": scheduleType/int
}
response.body = {
    "status": "OK",
    "schedule": {
        "id": string,
        "discription": string, 
        "location": string, 
        "startTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
        "endTime": string("Thu, 04 Apr 2019 08:00:00 GMT"), 
        "rotation": int,
        "userID": string,
        "type": scheduleType/int
    } //返回修改之后的schedule
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

