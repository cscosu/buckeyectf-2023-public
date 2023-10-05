from random_username.generate import generate_username
import random
import string

num = 100

usernames = generate_username(num)

class my_false:
    def __repr__(self) -> str:
        return "false"

users = []
for username in usernames:
    password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(30))
    session = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(30))
    users.append({
        "username": username,
        "password": password,
        "admin": my_false(),
        "session": session})

print(users)