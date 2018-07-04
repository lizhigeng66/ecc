
def modInverse(x, p):
    ret = 1
    exponent = p - 2
    while exponent != 0:
        if exponent & 1 == 1:
            ret = ret * x % p
        exponent = exponent >> 1
        x = x * x % p
    return ret
