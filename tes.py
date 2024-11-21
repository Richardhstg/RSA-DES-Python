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

# Fungsi enkripsi
def encrypt(plain_text, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in plain_text]
    return encrypted

# Fungsi dekripsi
def decrypt(cipher_text, private_key):
    d, n = private_key
    decrypted = ''.join([chr(pow(char, d, n)) for char in cipher_text])
    return decrypted

# Demo RSA
if __name__ == "__main__":
    random_id = random.randint(1000, 9999)  # Membatasi angka antara 100 hingga 999
    print(random_id)
    
    public_key, private_key = generate_keys()

    print(public_key)
    print(private_key)

    e, n = public_key
    
    result = ", ".join([str(e), str(n)])
    result = ", ".join([str(random_id), str(result)])
    print(result)
    
    split_result = result.split(", ")
    id_1 = int(split_result[0])
    e_1 = int(split_result[1])
    n_1 = int(split_result[2])
    
    print(id_1)
    print(e_1)
    print(n_1)
    
    print(f"client id {id_1}")
    
    # split_msg = message.split(", ")
    # e = int(split_msg[0])
    # n = int(split_msg[1])
    
    # pu_client = ", ".join([str(e), str(n)])
    
    
    # message = "79,3337"
    # print("Original Message:", message)

    # # Enkripsi pesan
    # encrypted_message = encrypt(message, public_key)
    # print("Encrypted Message:", encrypted_message)

    # # Dekripsi pesan
    # decrypted_message = decrypt(encrypted_message, private_key)
    # print("Decrypted Message:", decrypted_message)
