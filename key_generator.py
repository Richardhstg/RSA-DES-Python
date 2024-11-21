import random

# Fungsi untuk memeriksa apakah suatu bilangan adalah prima
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Fungsi untuk menghasilkan bilangan prima acak
def generate_large_prime(start=100, end=1000):
    prime = random.randint(start, end)
    while not is_prime(prime):
        prime = random.randint(start, end)
    return prime

# Fungsi untuk menghitung GCD (Greatest Common Divisor)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Fungsi untuk menghitung invers modular menggunakan Extended Euclidean Algorithm
def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Fungsi untuk menghitung kunci publik dan privat
def generate_keys():
    p = generate_large_prime()
    q = generate_large_prime()
    while q == p:  # Pastikan p dan q berbeda
        q = generate_large_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    # Pilih e (kunci publik) yang relatif prima terhadap phi
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Hitung d (kunci privat) sebagai invers modular dari e mod phi
    d = modular_inverse(e, phi)

    return (e, n), (d, n)

# public_key, private_key = generate_keys()
# print("Public Key:", public_key)
# print("Private Key:", private_key)