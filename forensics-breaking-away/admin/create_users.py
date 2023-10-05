import os
import random
import string
import lorem

files = lambda _: ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))
flag = 'YmN0Zns0MTFfdGgzX3VzM3JzX2I0YnlfZDBudF9tMzRuXzRueXRoMW5nfQ=='

beginning = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Portal</title>
</head>
<body>
    <div class="container mt-4">
        <h1>Users</h1>
    </div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">Admin Portal</a>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
"""

end = """
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <script src="/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

try:
    os.mkdir('users')
except:
    ...

users = set()
for i in range(10000):
    _random = files(i)
    with open('users/' + _random, 'w') as f:
        f.write(str(hash(i)))
        f.write(lorem.paragraph())
    users.add(f'/users/{_random}"> {_random} </a>')

with open('users.html', 'w') as f:
    f.write(beginning)
    for user in users:
        f.write(f'\n\t\t\t\t\t\t<a class="nav-link" href="{user}')
    f.write(end)