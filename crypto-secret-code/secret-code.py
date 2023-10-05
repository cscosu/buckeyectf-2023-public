from sys import exit

flag = "1:10:d0:10:42:41:34:20:b5:40:03:30:91:c5:e1:e3:d2:a2:72:d1:61:d0:10:e3:a0:43:c1:01:10:b1:b1:b0:b1:40:9"

str = input("Enter a string\n")
key = "snub_wrestle"

xored = ""
for i in range(max(len(key), len(str))):
    xored_value = ord(str[i%len(str)]) ^ ord(key[i%len(key)])
    xored = xored + ":".join("{:02x}".format(xored_value))

guess = ''.join(xored)

if guess == flag:
    print("You got the flag!")
else:
    print("Nope. Try again!")

exit()