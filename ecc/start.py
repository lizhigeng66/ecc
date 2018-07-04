from ecc import *

if __name__ == '__main__':
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    while True:
        print('-----*****-----choose option')
        print('-----*****-----1.generate key')
        print('-----*****-----2.encrypt')
        print('-----*****-----3.decrypt')
        print('-----*****-----4.exit')
        opt = input()
        if opt == '1':
            sk = gensk(n)
            print(f'-----*****-----private key: {sk}')
            sk = int(sk, 16)
            Pa, Pb = multiplication(sk, Gx, Gy, a, p)
            print(f'-----*****-----public key: {Pa},{Pb}')
        elif opt == '2':
            m = input('-----*****-----message:')
            print('-----*****-----public key:')
            Pa = input('-----*****-----x:')
            Pb = input('-----*****-----y:')
            C1, C2 = encrypt(m, Pa, Pb, Gx, Gy, a, p, n)
            print(f'-----*****-----ciphertext: C1x: {C1[0]},C1y:{C1[1]}')
            print(f'-----*****-----C2 {C2}')
        elif opt == '3':
            print('-----*****-----ciphertext')
            C1 = [0, 0]
            C1[0] = input('-----*****-----C1x:')
            C1[1] = input('-----*****-----C1y:')
            C2 = input('-----*****-----C2:')
            sk = input('-----*****-----private key:')
            sk = int(sk, 16)
            C2 = int(C2)
            m = decrypt(sk, C1, C2, Gx, Gy, a, p)
            print(f'-----*****-----message: {m}')
        else:
            break
