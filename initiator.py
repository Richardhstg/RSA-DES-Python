import socket
import threading
import random
from RSA import *
from DES import des_decryption, des_encryption
from key_generator import generate_keys

def main():    
    pu_pka = (125033, 541279)
    client_id = random.randint(1000, 9999)

    public_key, private_key = generate_keys()

    host = socket.gethostname()
    port = 5000

    client = socket.socket()
    client.connect((host, port)) 
    
    print(client_id)
    print(f"public key: {public_key}")
    
    # kirim public key ke PKA
    e, n = public_key
    pu = ", ".join([str(e), str(n)])
    pu_with_id = ", ".join([str(client_id), str(pu)])
    store_pu = rsa_encrypt(pu_with_id, pu_pka)
    client.send(store_pu.encode())
    
    print("Berhasil kirim Public Key ke PKA")
         
    
    while True:
        print("1. Request public key client lain")
        print("2. Mulai Chat")
        print("3. Exit")  
                
        message = input(">> ")
        if message == "3":
            break
        if message == "1":
            message = rsa_encrypt(message, pu_pka)
            client.send(message.encode())

            id_dest = input("ID responder :")
            id_dest = str(id_dest)
            
            message = rsa_encrypt(id_dest, pu_pka)
            client.send(message.encode())
            
            enc_pu_dest = client.recv(1024).decode()
            
            pu_dest = rsa_decrypt(enc_pu_dest, pu_pka)
            
            print(f"2. Public Key Responder : {pu_dest}")
            
            e, n = map(int, pu_dest.split(", "))
            
            pu_dest = e, n
            
            # kirim id dan n1 ke dest (di enkripsi dengan pu_dest)
            
            n1 = random.randint(1000, 9999)
            
            validate = ", ".join([str(client_id), str(n1)])
            
            enc_validate = rsa_encrypt(validate, pu_dest)
            
            client.send(enc_validate.encode())

            # terima n1 n2
            enc_n1_n2 = client.recv(1024).decode()
            n1_n2 = rsa_decrypt(enc_n1_n2, private_key)
            print(f"N1 N2 {n1_n2}")
            
            split_msg = n1_n2.split(", ")
            n1_str = split_msg[0]
            n1_check = int(n1_str)
            
            n2_str = split_msg[1]
            
            if(n1 != n1_check):
                break
            
            # last validation
            last_val_request = rsa_encrypt("last_validation", pu_pka)
            client.send(last_val_request.encode())
            
            message = rsa_encrypt(n2_str, pu_dest)
            client.send(message.encode())
            
            client.close()
            print("[INFO] Koneksi ke PKA ditutup.")
            
        if message == "2":
            host = socket.gethostname()
            port = 2024

            client = socket.socket()
            client.connect((host, port))
            
            des_key = input("Key untuk DES : ")
            pu_key_dest = input("Key Public Penerima: ")
            
            e, n = map(int, pu_key_dest.split(", "))
            pu_dest = e, n
            
            enc_1_des_key = rsa_encrypt(des_key, private_key)
            enc_2_des_key = rsa_encrypt(enc_1_des_key, pu_dest)
            
            client.send(enc_2_des_key.encode())
            
            
            

if __name__ == "__main__":
    main()
