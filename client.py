import socket
import threading
import random
from RSA import *
from DES import des_decryption, des_encryption
from key_generator import generate_keys

pu_pka = (125033, 541279)


def receive_messages(client_socket, private_key):
    """Fungsi untuk menerima pesan dari server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            message = rsa_decrypt(message, pu_pka)
            print(f"\r[Pesan] {message}\n>> ", end="")
        except:
            print("[INFO] Koneksi ke server terputus.")
            break

def main():
    # client_id = random.randint(1000, 9999)
    public_key, private_key = generate_keys()

    host = socket.gethostname()
    port = 5000

    client = socket.socket()
    client.connect((host, port)) 

    # kirim public key ke PKA
    e, n = public_key
    pu = ", ".join([str(e), str(n)])
    # id_pu = ", ".join([str(client_id), str(pu)])
    store_pu = rsa_encrypt(pu, pu_pka)
    client.send(store_pu.encode())
    
    print("Berhasil kirim Public Key ke PKA")
    
    # Thread untuk menerima pesan dari pka server
    thread = threading.Thread(target=receive_messages, args=(client, private_key))
    thread.start()    
    
    
    # request public key client lain
    print("1. Request public key client lain")
    print("2. Mulai Chat")
    print("3. Exit")
    
    while True:
        message = input(">> ")
        if message == "3":
            break
        message = rsa_encrypt(message, pu_pka)
        client.send(message.encode())
    client.close()
    print("[INFO] Koneksi ditutup.")

if __name__ == "__main__":
    main()
