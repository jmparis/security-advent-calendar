from sympy import mod_inverse

p = 829964450046321974947
q = 648876506515007420328921808692076639722017679557003069

n = p * q
e = 65537

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)

print(d)