import random
import hashlib


def Exponentiation(a, g, p):
    e = a % (p - 1)
    if e == 0:
        return 1
    e_2 = bin(e)[3:]
    x = g
    for i in e_2:
        x = x ** 2
        if i == '1':
            x = g * x
    return x % p


def generateAB(p):
    seed = random.randint(0x000000000000000000000000, 0xffffffffffffffffffffffff)
    # print(hex(seed))
    seed = hex(seed)
    H = hashlib.sha256(seed.encode('UTF-8')).hexdigest()
    b = int(H, 16) % p
    a = random.randint(0, p)
    tmp = 4 * (a ** 2) + 27 * (b ** 3)
    if tmp % p == 0:
        seed, a, b = generateAB(p)
    return seed, a, b


def verify(seed, b, p):
    H = hashlib.sha256(seed.encode('UTF-8')).hexdigest()
    R = int(H, 16)
    r = R % p
    if r == b:
        return True
    else:
        return False


def generateG(p, a, b):
    x = random.randint(0, p)
    tmp = x ** 3 + a * x + b
    if tmp % p == 0:
        return x, 0
    g = tmp % p
    y = modPower(p, g) % p
    if y == False:
        x, y = generateG(p, a, b)
    return x, y


def modPower(p, g):
    if (p - 3) % 4 == 0:
        j = (p - 3) % 4
        u_1 = (p - 3) // 4
        y = Exponentiation(u_1 + 1, g, p)
        z = Exponentiation(2, y, p)
        if z == g:
            return y
        return False
    elif (p - 5) % 8 == 0:
        u_2 = (p - 5) // 8
        z = Exponentiation(2 * u_2 + 1, g, p)
        if (z - 1) % p == 0:
            y = Exponentiation(u_2 + 1, g, p)
            return y
        elif (z + 1) % p == 0:
            y = (2 * g * Exponentiation(u_2, 4 * g, p))
            return y
        return False
    elif (p - 1) % 8 == 0:
        u_3 = (p - 1) // 8
        Y = g
        X = random.randint(0, p)
        U, V = lucas(p, X, Y, 4 * u_3 + 1)
        if ((V ** 2) - 4 * Y) % p == 0:
            return (V / 2) % p
        if U % p != 1 and U % p != p - 1:
            return False


def lucas(p, X, Y, k):
    tmp = X ** 2 - 4 * Y
    k_2 = bin(k)[3:]
    U = 1
    V = X
    for i in k_2:
        U, V = (U * V) % p, (((V ** 2) + tmp(U ** 2)) / 2) % p
        if i == '1':
            U, V = ((X * U + V) / 2) % p, ((X * V + tmp * U) / 2) % p
    return U, V


if __name__ == '__main__':
    # p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    p = 10000141
    seed, a, b = generateAB(p)
    Gx, Gy = generateG(p, a, b)
    print(a)
    print(b)
    print(Gx)
    print(Gy)
    result = Gx ** 3 + a * Gx + b
    print(result % p)
    print(Gy ** 2 % p)
    # print(verify(seed, b, p))
