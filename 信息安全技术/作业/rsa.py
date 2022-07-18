import time
import binascii
from makeprime import make_prime


# 扩展欧几里得 求解 ax + by = 1 中的 x 和 y
def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        r, x_, y_ = ext_gcd(b, a % b)
        x = y_
        y = x_ - a // b * y_
        return r, x, y


# 快速幂 计算 (base ^ exponent) mod n
def exp_mod(base, exponent, n):
    # 取 exponent 的二进制并倒置
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)

    # 快速幂
    base_array = [base]
    for _ in range(r - 1):
        next_base = (base * base) % n
        base_array.append(next_base)
        base = next_base
    res = 1
    for i in range(len(base_array)):
        if int(bin_array[i]):
            res = (res * base_array[i]) % n
    return res % n


# 字符串转整形
def str_to_int(text):
    if type(text) is not str:
        text = str(text)
    text = bytes(text, encoding='utf-8')
    return int(binascii.b2a_hex(text), 16)


# 整形转字符串
def int_to_str(num):
    return str(binascii.a2b_hex(hex(num)[2:]), encoding='utf-8')


# 加密
def encrypt_with_pub_key(plaintext, pub_key):
    m = str_to_int(plaintext)
    e, n = pub_key
    return exp_mod(m, e, n)


# RSA
class RSA:
    def __init__(self, p=None, q=None):
        if p is None:
            p = make_prime(1024)
        if q is None:
            q = make_prime(1024)

        # 生成公私钥
        n = p * q
        f = (p - 1) * (q - 1)
        e = 65537
        _, d, _ = ext_gcd(e, f)
        if d < 0:
            d += f
        self._pub_key = (e, n)
        self._pri_key = (d, n)

    def get_pub_key(self):
        return self._pub_key

    # 加密
    def encrypt(self, plaintext):
        m = str_to_int(plaintext)
        e, n = self._pub_key
        return exp_mod(m, e, n)

    # 解密
    def decrypt(self, ciphertext):
        d, n = self._pri_key
        m = exp_mod(ciphertext, d, n)
        return int_to_str(m)


# 用中国剩余定理优化的 RSA
class CRT_RSA:
    def __init__(self, p=None, q=None):
        if p is None:
            p = make_prime(1024)
        if q is None:
            q = make_prime(1024)

        # 生成公私钥
        n = p * q
        e = 65537
        self._pub_key = (e, n)

        _, dP, _ = ext_gcd(e, p - 1)
        _, dQ, _ = ext_gcd(e, q - 1)
        _, qInv, _ = ext_gcd(q, p)
        if dP < 0:
            dP += p - 1
        if dQ < 0:
            dQ += q - 1
        if qInv < 0:
            qInv += p
        self._pri_key = (p, q, dP, dQ, qInv)

    def get_pub_key(self):
        return self._pub_key

    # 加密
    def encrypt(self, plaintext):
        m = str_to_int(plaintext)
        e, n = self._pub_key
        return exp_mod(m, e, n)

    # 解密
    def decrypt(self, ciphertext):
        p, q, dP, dQ, qInv = self._pri_key
        m1 = exp_mod(ciphertext, dP, p)
        m2 = exp_mod(ciphertext, dQ, q)
        h = (qInv * (m1 - m2)) % p
        m = m2 + h * q
        return int_to_str(m)

if __name__ == "__main__":

    p = make_prime(1024)
    q = make_prime(1024)
    print("P:", p)
    print("Q:", q)

    # 明文
    m = "Shinde, G. N., and H. S. Fadewar. 'Faster RSA algorithm for decryption using Chinese remainder theorem'. " \
        "ICCES: International Conference on Computational & Experimental Engineering and Sciences. Vol. 5. No. 4. 2008."
    print("\nPlaintext:\n", m)

    print("\n-[RSA]---------------------------------------------------------------------------------------------------")
    # 生成 RSA 公私钥
    myRSA = RSA(p=p, q=q)
    myPubKey = myRSA.get_pub_key()
    print("\nRSA Public Key:", myPubKey)

    # 加密
    c = myRSA.encrypt(m)
    # or
    # c = encrypt_with_pub_key(m, myPubKey)
    print("Ciphertext:", c)

    # 解密
    ss = time.time()
    d = myRSA.decrypt(c)
    rsa_time = time.time() - ss

    print("\nDecrypt Result:", d)
    print("TimeCost of Decrypt: %.5f s" % rsa_time)
    if m == d:
        print("PlainText and Decrypt Result is the same")

    print("\n-[CRT-RSA]-----------------------------------------------------------------------------------------------")
    # 生成 RSA 公私钥
    myCRT_RSA = CRT_RSA(p=p, q=q)
    myCRT_PubKey = myCRT_RSA.get_pub_key()
    print("\nCRT-RSA Public Key:", myCRT_PubKey)

    # 加密
    c = encrypt_with_pub_key(m, myCRT_PubKey)
    print("Ciphertext:", c)

    # 解密
    ss = time.time()
    d = myCRT_RSA.decrypt(c)
    crt_rsa_time = time.time() - ss

    print("\nDecrypt Result:", d)
    print("TimeCost of Decrypt: %.5f s" % crt_rsa_time)
    if m == d:
        print("PlainText and Decrypt Result is the same")

    print("\n[Time of CRT-RSA Decrypt] / [Time of RSA Decrypt] = %.2f%%" % (crt_rsa_time / rsa_time * 100))