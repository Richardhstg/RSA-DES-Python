def rsa_encrypt(plain_text, public_key):
    e, n = public_key
    encrypted = [str(pow(ord(char), e, n)) for char in plain_text]
    return ",".join(encrypted)

def rsa_decrypt(cipher_text, private_key):
    d, n = private_key
    encrypted_values = map(int, cipher_text.split(","))
    decrypted = ''.join([chr(pow(value, d, n)) for value in encrypted_values])
    return decrypted
