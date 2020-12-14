#用来做一些闲杂测试，忽略即可

from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 

user_data = {'code':0, 'data': {}}
name = 'hi'
user_data['data']['msg'] = 'hi"' + name + '"hi'


WHERE users_v1.username = %s
2020-12-15 00:08:09,421 INFO sqlalchemy.engine.base.Engine ('Dave',)
2020-12-15 00:08:09,742 INFO sqlalchemy.engine.base.Engine INSERT INTO users_v1 (username, email, password, avater, motto) VALUES (%s, %s, %s, %s, %s)
2020-12-15 00:08:09,744 INFO sqlalchemy.engine.base.Engine ('Dave', 'dave@pku.edu.cn', 'pbkdf2:sha256:50000$PWmSUhb1$ead10acd6f85bbc75b541121ef2d59251c80a0ab81803b9eb5089f6cd17b9d8b', None, None)
2020-12-15 00:08:09,760 INFO sqlalchemy.engine.base.Engine COMMIT
2020-12-15 00:08:09,779 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
2020-12-15 00:08:09,781 INFO sqlalchemy.engine.base.Engine SELECT users_v1.id AS users_v1_id, users_v1.username AS users_v1_username, users_v1.email AS users_v1_email, 
users_v1.password AS users_v1_password, users_v1.avater AS users_v1_avater, users_v1.motto AS users_v1_motto
FROM users_v1
WHERE users_v1.id = %s
2020-12-15 00:08:09,783 INFO sqlalchemy.engine.base.Engine (2,)
2020-12-15 00:08:09,786 INFO sqlalchemy.engine.base.Engine ROLLBACK



2020-12-15 00:03:30,249 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
2020-12-15 00:03:30,250 INFO sqlalchemy.engine.base.Engine SELECT users_v1.id AS users_v1_id, users_v1.username AS users_v1_username, users_v1.email AS users_v1_email, users_v1.password AS users_v1_password, users_v1.avater AS users_v1_avater, users_v1.motto AS users_v1_motto
FROM users_v1
WHERE users_v1.username = %s
2020-12-15 00:03:30,262 INFO sqlalchemy.engine.base.Engine ('rwy',)
2020-12-15 00:03:30,486 INFO sqlalchemy.engine.base.Engine INSERT INTO users_v1 (username, email, password, avater, motto) VALUES (%s, %s, %s, %s, %s)
2020-12-15 00:03:30,490 INFO sqlalchemy.engine.base.Engine ('rwy', '12345678@pku.edu.cn', 'pbkdf2:sha256:150000$9N0jJwvV$9702ce3d7eca2acfe9ddda7b8af12e7f4139aa512023e411518f5e1fc8285f84', None, None)
2020-12-15 00:03:30,503 INFO sqlalchemy.engine.base.Engine ROLLBACK

