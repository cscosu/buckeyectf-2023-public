import requests
import string
alphabet = string.digits + string.ascii_letters + '_{}'

# solve script doesn't entirely work but mostly

def encrypt(s):
    resp = requests.get("http://localhost:5000/encrypt", {"message": s})
    print(s.decode())
    print(resp.text)
    return bytes.fromhex(resp.text)

def get_blocks(s):
    return [s[i:i+16] for i in range(0, len(s), 16)]

def do(curr):
    blocks = get_blocks(curr)
    if blocks == []:
        blocks = [b'']
    padding = b"A" * (15 - len(blocks[-1]))
    things1 = [padding + blocks[-1] + c.encode() for c in alphabet]
    things = {
        get_blocks(encrypt(padding + blocks[-1] + c.encode()))[0]: c.encode()
        for c in alphabet
    }
    magic = get_blocks(encrypt(b"A"*(15 - len(blocks[-1]))))
    return things[magic[0]]

curr = b''
while not curr.endswith(b'}'):
    print(curr)
    curr += do(curr)

# print(things[bs[0]])