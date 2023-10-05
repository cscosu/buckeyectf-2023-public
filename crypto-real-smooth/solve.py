from collections import Counter
from Crypto.Util.strxor import strxor

lines = open("database.txt")
lines = [bytes.fromhex(line) for line in lines]
for i, x in enumerate(lines):
    assert len(x) == 18
most_common = Counter(lines).most_common(1)[0][0]


passwords = open("rockyou.txt", "br")
key_stream = bytes()
for password in passwords:
    key_stream = strxor(most_common, password.ljust(18))
    for x in lines:
        if strxor(key_stream, x).find(b"btcf{") >= 0:
            output = [
                strxor(key_stream, x)
                for x in lines
                if strxor(key_stream, x).find(b"{") >= 0
                or strxor(key_stream, x).find(b"}") >= 0
            ]
            print(output)
            exit()
            break
