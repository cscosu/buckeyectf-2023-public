#!/usr/bin/env python3

flag = "bctf{Aw_$hucK$_Y0ur3_m@k1Ng_m3_bLu$h}"
otp = [161, 143, 215, 178, 242, 250, 72, 57, 107, 194, 146, 16, 88, 68, 101, 140, 74, 117, 86, 11, 102, 81, 104, 137, 141, 12, 253, 141, 103, 34, 223, 15, 202, 143, 155, 37, 185]




def enc_flag(data):
    data = [ord(c) for c in data]

    data = [x ^ y for x, y in zip(data, otp)]

    data = [c ^ 0x69 for c in data]

    flag2 = data.copy()
    for k in range(1, len(data)):
        flag2[k] = data[k] ^ flag2[k-1]

    return flag2

def dec_flag(data):
    enc2 = data.copy()
    for k in reversed(range(1, len(data))):
        #print(f"{enc2[k]}")
        enc2[k] = enc2[k] ^ enc2[k-1]

    enc2 = [c ^ 0x69 for c in enc2]

    enc2 = [x ^ y for x, y in zip(enc2, otp)]


    return enc2




print(f"flag: {flag}")
print(f"flag: { [ord(c) for c in flag]}")

enc = enc_flag(flag)
print(f"flag enc: {enc}")

dec = dec_flag(enc)
print(f"flag dec: {dec}")