import random
from random import randint

# makeprime.py Copy From:
# https://blog.csdn.net/qq_36944952/article/details/103973849

# w表示希望产生位数，生成目标位数的伪素数
def pro_bin(w):
    li = ['1']
    for _ in range(w - 2):
        c = random.choice(['0', '1'])
        li.append(c)
    li.append('1')  # 最低位定为1
    res = int(''.join(li), 2)
    return res


def x_n_mod_p(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []

    pre_base = base
    base_array.append(pre_base)

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n
        base_array.append(next_base)
        pre_base = next_base

    a_w_b = __multi(base_array, bin_array, n)
    return a_w_b % n


def __multi(array, bin_array, n):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n
    return result


def miller_rabin(a, p):
    if x_n_mod_p(a, p - 1, p) == 1:
        u = (p - 1) >> 1
        while (u & 1) == 0:
            t = x_n_mod_p(a, u, p)
            if t == 1:
                u = u >> 1
            else:
                if t == p - 1:
                    return True
                else:
                    return False
        else:
            t = x_n_mod_p(a, u, p)
            if t == 1 or t == p - 1:
                return True
            else:
                return False
    else:
        return False


# k为测试次数，p为待测奇数
def test_miller_rabin(p, k):
    while k > 0:
        a = randint(2, p - 1)
        if not miller_rabin(a, p):
            return False
        k = k - 1
    return True


# 产生 w 位的素数
def make_prime(w):
    while 1:
        d = pro_bin(w)
        # 伪素数附近50个奇数都没有真素数的话，重新再产生一个伪素数
        u = False
        b = 0
        for i in range(50):
            u = test_miller_rabin(d + 2 * i, 5)
            if u:
                b = d + 2 * i
                break
            else:
                continue
        if u:
            return b
        else:
            continue


if __name__ == "__main__":  # 测试
    print(make_prime(1024))

