from utils.db import mysql
from utils.tools import hash_password

user = mysql.save(
    model="users",
    username='evalli',
    password_hash=hash_password('p4ssw0rd'),
    displayname='Edgar Valli',
    active=1
)

print(user)