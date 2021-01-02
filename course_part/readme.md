文件库

| id   | filename | score | uploader | description | course |
| ---- | -------- | ----- | -------- | ----------- | ------ |
| int  | str      | int   | int      | str         | int    |

课程库

| id   | name | info |
| ---- | ---- | ---- |
| int  | str  | str  |

笔记库

| id   | filename | score | uploader | description | course |
| ---- | -------- | ----- | -------- | ----------- | ------ |
| int  | str      | int   | int      | str         | int    |

ddl库

| id   | description | location | startTime | endTime | rotation | userID | schedule Type |
| ---- | ----------- | -------- | --------- | ------- | -------- | ------ | ------------- |
| int  | str         | str      | time      | time    | bool     | int    | int           |

用户库

| id   | isAdmin | username | email | password    | avatar | motto |
| ---- | ------- | -------- | ----- | ----------- | ------ | ----- |
| int  | bool    | str      | str   | str（密文） | img    | str   |

