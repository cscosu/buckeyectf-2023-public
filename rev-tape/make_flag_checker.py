
STACK_SIZE = 64
#FLAG = b"ABCD"
FLAG = b"bctf{Y0u_Sp1n_M3_R1gHt_R0uNd}"
# Evil, make the key values overlap with the instruction bytes
KEY = b"\x40\x32\x41\x10\x78\x69\x21"

def add_instructions(instructions):
    count = 0
    out = ""
    for line in instructions:
        out += line + "\n"
        if line and line[0] != "#":
            count += 1
            if "PUSH" in line:
                count += 1

    return (out, count)

def main():
    out, count = read_in()
    print(out)

    amt = len(FLAG)
    for idx in range(amt):
        key_byte = KEY[idx % len(KEY)]
        print("DUP")
        print("PUSH =" + hex(key_byte))
        out, count = xor()
        print(out)

        
        invalid_out, invalid_count = make_invalid(idx)

        check_out, check_count = jump_if_equal(invalid_count, FLAG[len(FLAG) - idx - 1] ^ key_byte)

        print(check_out)
        print(invalid_out)

    print("POP\n" * (STACK_SIZE - 4 - amt))

    correct_out, correct_count = print_text("Correct!")

    invalid_out, invalid_count = print_text("Invalid Flag!")
    invalid_out += "EXIT\n"
    invalid_count += 1

    check_out, check_count = jump_if_equal(invalid_count, 187)

    print(check_out)
    print(invalid_out)
    print(correct_out)

    





def make_invalid(idx):
    instructions = []
    instructions.extend(["POP"] * (STACK_SIZE - 5 - idx))
    instructions.append("PUSH =0x01")
    instructions.append("ADD")
    instructions.extend(["POP"] * (5 + idx))


    out, count = add_instructions(instructions)
    return out, count


    # print("PUSH =0x54")
    # correct_out, correct_count = print_text("Correct!")
    # correct_out += "EXIT\n"
    # correct_count += 1
    # invalid_out, invalid_count = print_text("Invalid Flag")
    # print(check_out)
    # print(correct_out)
    # print(invalid_out)

# def main():
#     print("PUSH =0x54")
#     correct_out, correct_count = print_text("Correct!")
#     invalid_out, invalid_count = print_text("Invalid Flag")
#     invalid_out += "EXIT\n"
#     invalid_count += 1
#     check_out, check_count = jump_if_equal(invalid_count, 0x53)
#     print(check_out)
#     print(invalid_out)
#     print(correct_out)
#     print("PRINTH")

def read_in():
    read_instructions = []
    read_instructions.extend(["GET"] * len(FLAG))

    out, count = add_instructions(read_instructions)
    return out, count

# def main():
#     print("""PUSH =0x54
# DUP
# PUSH =0x82""")
#     out, count = xor()
#     print(out)
#     print()
#     out, count = print(b"Correct!")

#     out, count = print(b"Invalid Flag")
#     print(out)
#     print("PRINTH")

# A must be in #0 and #1
# B must be in #2
# A ^ B
def xor():
    instruction = [
        "# xor",
        "DUP",
        "POP",
        "NAND",
        "DUP"
    ]
    instruction.extend(["POP"] * (STACK_SIZE - 1))

    instruction.extend([
        "NAND",
        "POP",
        "NAND",
        "DUP"
    ])
    instruction.extend(["POP"] * (STACK_SIZE - 1))

    instruction.append("NAND")

    out, count = add_instructions(instruction)

    return out, count

def jump_if_not_equal(offset, value: int):
    instructions2 = []
    instructions2.extend(["POP"] * (STACK_SIZE + 2))
    instructions2.append("PUSH =" + hex(value))
    instructions2.extend(["POP"] * (STACK_SIZE - 1))
    instructions2.append("SUB")
    instructions2.append("PUSH =" + hex(offset))
    instructions2.append("BNZ")

    out2, count2 = add_instructions(instructions2)

    instructions = []
    instructions.append("DUP")
    instructions.append("PUSH =" + hex(value))
    instructions.append("SUB")
    instructions.append("PUSH =" + hex(count2 + offset))
    instructions.append("BNZ")

    out, count = add_instructions(instructions)

    return out+out2, count + count2

def jump_if_equal(offset, value: int):
    instructions2 = []
    instructions2.extend(["POP"] * (STACK_SIZE + 2))
    instructions2.append("PUSH =" + hex(value))
    instructions2.extend(["POP"] * (STACK_SIZE - 1))
    instructions2.append("SUB")
    instructions2.append("PUSH =" + hex(offset))
    instructions2.append("BZ")

    out2, count2 = add_instructions(instructions2)

    instructions = []
    instructions.append("DUP")
    instructions.append("PUSH =" + hex(value))
    instructions.append("SUB")
    instructions.append("PUSH =" + hex(count2))
    instructions.append("BNZ")

    out, count = add_instructions(instructions)

    return out+out2, count + count2


def print_text(text: str):
    text = text.encode()
    instructions = []
    for b in text:
        instructions.append("PUSH =" + hex(b))
        instructions.append("PRINT")

    out, count = add_instructions(instructions)

    return out, count


if __name__ == "__main__":
    main()