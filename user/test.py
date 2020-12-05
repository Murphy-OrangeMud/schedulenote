from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 

s = ['1', '1', '1']
for i in s:
    a = generate_password_hash(i)
    print(a)
    print(check_password_hash(a, i))
