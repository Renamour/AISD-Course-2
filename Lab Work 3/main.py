import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("Ошибка: e и phi(n) не взаимно простые!")
    d = modinv(e, phi)
    return ((n, e), (n, d))

def encrypt(public_key, plaintext):
    n, e = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

def decrypt(private_key, ciphertext):
    n, d = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext

p = 61
q = 53
e = 17
public_key, private_key = generate_keypair(p, q, e)

user_input = input("Введите сообщение для шифрования: ")
encrypted_message = encrypt(public_key, user_input)

decrypted_message = decrypt(private_key, encrypted_message)

print("Исходное сообщение:", user_input)
print("Зашифрованное сообщение:", encrypted_message)
print("Расшифрованное сообщение:", decrypted_message)