import random
from main import encrypt
from Crypto.Random import get_random_bytes
from collections import Counter
from Crypto.Util.strxor import strxor

max_length = 18

lines = open("passwords.txt", "rb").readlines()
lines = [
    line
    for line in lines
    if len(line) <= max_length and line.find(b"{") == -1 and line.find(b"}") == -1
]
lines = [line.ljust(max_length) for line in lines]
lines = [
    x
    for line in lines
    for x in [line]
    * random.choice(
        [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            2,
            3,
            4,
            5,
        ]
    )
]
lines = [
    x
    for line in lines
    for x in [line] * random.choice([1, 2, 3, 4, 5])
    if len(x) == max_length
]
lines.append(b"btcf{w3_d0_4_l177l")
lines.append(b"3_kn0wn_pl41n73x7}")

random.shuffle(lines)

most_common = Counter(lines).most_common(1)[0][0]
print(most_common)

key = get_random_bytes(32)
nonce = get_random_bytes(8)

key_stream = strxor(
    encrypt(key, nonce, b"password".ljust(max_length)), b"password".ljust(max_length)
)
print("key stream: ", key_stream)

cipher_text = [encrypt(key, nonce, line) for line in lines]
open("database.txt", "w").writelines("\n".join(c.hex() for c in cipher_text))
