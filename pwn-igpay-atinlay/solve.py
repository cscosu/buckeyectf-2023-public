from pwn import *

c = remote('127.0.0.1', 1337)

c.sendline("❤️")

print(c.recvall().decode())