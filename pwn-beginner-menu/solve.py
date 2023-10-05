from pwn import *
import pwnlib

if args.REMOTE:
    io = remote("chall.pwnoh.io", 13371)
elif args.GDB:
    io = gdb.debug("./menu")
else:
    io = process("./menu")

io.recvuntil("Quit\n")
io.sendline("hello")

print(io.recvall())
