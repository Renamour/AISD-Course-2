from math import sqrt
import random
from random import randint as rand
APP_RSA_PUBLIC_KEY = (28147, 55973)
APP_RSA_PRIVATE_KEY = (46483, 55973)


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


def isprime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
    return True

p = 223
q = 251


def generate_keypair(p, q, keysize):
    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [2]
    start = 1 << (keysize // 2 - 1)
    stop = 1 << (keysize // 2 + 1)

    if start >= stop:
        return []

    for i in range(3, stop + 1, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)

    while primes and primes[0] < start:
        del primes[0]

    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_values = [q for q in primes if nMin <= p * q <= nMax]
        if q_values:
            q = random.choice(q_values)
            break
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while True:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        d = mod_inverse(e, phi)
        if g == 1 and e != d:
            break
    return (e, n), (d, n)


def encrypt(msg_plaintext, package=APP_RSA_PUBLIC_KEY):
    e, n = (int(package[0]), int(package[1]))
    msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
    return msg_ciphertext


def decrypt(msg_ciphertext, package=APP_RSA_PRIVATE_KEY):
    d, n = (int(package[0]), int(package[1]))
    msg_plaintext = [chr(pow(c, d, n)) for c in [ord(x) for x in msg_ciphertext]]
    return ''.join(msg_plaintext)

