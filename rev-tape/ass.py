#!/usr/bin/python3

import argparse

parse = argparse.ArgumentParser()
parse.add_argument("in_file", help="Path of file to assemble")
parse.add_argument("out_file", help="Path of file to assemble")

parse_args = parse.parse_args()

    
opcodes = {
    "PUSH": 0x00,
    "POP": 0x01,
    "DUP": 0x02,

    "BZ": 0x10,
    "BNZ": 0x12,

    "ADD": 0x20,
    "SUB": 0x21,
    "MULT": 0x22,
    "NAND": 0x24,

    "PVT": 0x30,

    "PRINT": 0x40,
    "PRINTH": 0x41,
    "GET": 0x42,
    "GETH": 0x43,

    "EXIT": 0x50,
}

def die():
    exit(-1)

with open(parse_args.in_file, "r") as file:
    print(f"Assmbling from {file.name}")
    with open(parse_args.out_file, "wb") as out:
        print(f"Assmbling to {out.name}")
        line_num = 0
        for line in file:
            line_num = line_num + 1
            if not line: continue
            if line[0] == "#": continue

            parts = line.split()
            if not parts: continue

            current_instruction = parts[0]
            if current_instruction not in opcodes:
                print(f"Invalid instruction '{current_instruction} on line {line_num}'")
                die()

            current_opcode = opcodes[current_instruction]
            out.write(current_opcode.to_bytes(1))
            if current_instruction == "PUSH":
                # Special for push
                if len(parts) != 2 or parts[1][0] != "=":
                    print(f"PUSH has invalid arguments: {parts}")
                    die()
                
                constant_str = parts[1][1:]
                value = int(constant_str, 16)
                out.write(value.to_bytes(1))

print("Done!")
                

        