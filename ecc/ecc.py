# y^2=x^3+ax+b
import random
import reverse
import binascii


def gensk(n):
    secretkey = random.randint(0, n)
    return hex(secretkey)


def sameplus(x1, y1, a, p):
    if x1 == 0 and y1 == 0:
        return 0, 0
    k = ((3 * x1 * x1 + a) * reverse.modInverse(2 * y1, p)) % p
    x = (k ** 2 - 2 * x1) % p
    y = (k * (x1 - x) - y1) % p
    return x, y


def diffplus(x1, y1, x2, y2, a, p):
    if x1 == 0 and y1 == 0:
        return x2, y2
    elif x2 == 0 and y2 == 0:
        return x1, y1
    else:
        k = ((y2 - y1) * reverse.modInverse(x2 - x1, p)) % p
        x = (k ** 2 - x1 - x2) % p
        y = (k * (x1 - x) - y1) % p
        return x, y


def plus(x1, y1, x2, y2, a, p):
    if x1 == x2 and y1 == y2:
        return sameplus(x1, y1, a, p)
    else:
        return diffplus(x1, y1, x2, y2, a, p)


def multiplication(sk, Gx, Gy, a, p):
    Q = [0, 0]
    k = bin(sk)[2:][::-1]
    for j in range(len(bin(sk)[2:]) - 1, -1, -1):
        Q[0], Q[1] = sameplus(Q[0], Q[1], a, p)
        if k[j] == '1':
            Q[0], Q[1] = plus(Q[0], Q[1], Gx, Gy, a, p)
    #print(hex(Q[0]) + ',' + hex(Q[1]))
    return hex(Q[0]), hex(Q[1])


def encrypt(m, Pa, Pb, Gx, Gy, a, p, n):
    x = int(Pa, 16)
    y = int(Pb, 16)
    r = random.randint(0, n)
    Cx1, Cy1 = multiplication(r, Gx, Gy, a, p)
    Cx2, Cy2 = multiplication(r, x, y, a, p)
    # print(hash(Cx2 + Cy2))
    m_16 = binascii.b2a_hex(m.encode('UTF-8'))
    m_2 = int(m_16, 16)
    # print(m_2)
    C2 = m_2 ^ hash(Cx2 + Cy2)
    return [Cx1, Cy1], C2


def decrypt(sk, C1, C2, Gx, Gy, a, p):
    x = int(C1[0], 16)
    y = int(C1[1], 16)
    x, y = multiplication(sk, x, y, a, p)
    m_10 = C2 ^ hash(x + y)
    m_16 = hex(m_10)
    # print(m_16)
    m = binascii.a2b_hex(m_16[2:])
    return m.decode('ascii')


# if __name__ == '__main__':
#     p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
#     a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
#     b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
#     n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
#     Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
#     Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
#     sk = int(gensk(n), 16)
#     # p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
#     # a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
#     # b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
#     # n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
#     # Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
#     # Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
#     # sk = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
#     print(sk)
#     Pa, Pb = multiplication(sk, Gx, Gy, a, p)
#     print(Pa + ',' + Pb)
#     C1, C2 = encrypt('helloewwewrdffreretetrttsdsdsdsdsds', Pa, Pb, Gx, Gy, a, p, n)
#     print(C1)
#     print(C2)
#     m = decrypt(sk, C1, C2, Gx, Gy, a, p)
#     print(m)
