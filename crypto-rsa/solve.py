c = 414434392594516328988574008345806048885100152020577370739169085961419826266692

p = 3782335750369249076873452958462875461053
q = 9038904185905897571450655864282572131579
e = 65537

n = p * q
et = (p - 1) * (q - 1)
d = pow(e, -1, et)

m = pow(c, d, n)

print(m.to_bytes(100, "big"))