flag = "110d01042413420b540033091c5e1e3d2a272d161d010e3a043c10110b1b1b0b1409"
flag = bytes.fromhex(flag)

key = "snub_wrestle"

xored = []
for i in range(max(len(key), len(flag))):
    xored_value = flag[i % len(flag)] ^ ord(key[i % len(key)])
    xored.append(hex(xored_value)[2:])

guess = "".join(xored)
print(guess)
guess = bytes.fromhex(guess)
guess = guess.decode("utf-8")
print(guess)
