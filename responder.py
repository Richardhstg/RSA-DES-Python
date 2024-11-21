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
        validate = client.recv(1024).decode()
        if not validate:
            return
        
        validate_request = rsa_decrypt(validate, private_key)
        
        print(f"3. ID Initiator dan N1 : {validate_request}")
        
        split_msg = validate_request.split(", ")
        
        another_client_id = split_msg[0]
        n1_str = split_msg[1]
        n1 = int(n1_str)
        n2 = random.randint(1000, 9999)
        
        print(f"Validate Request from user {another_client_id}")
        
        request = rsa_encrypt("1", pu_pka)
        client.send(request.encode())
        
        another_client_id = str(another_client_id)
        message = rsa_encrypt(another_client_id, pu_pka)
        client.send(message.encode())
        
        enc_pu_dest = client.recv(1024).decode()
        
        pu_dest = rsa_decrypt(enc_pu_dest, pu_pka)
        
        print(f"5. Public Key Initiator : {pu_dest}")
        
        # send n1 n2
        
        e, n = map(int, pu_dest.split(", "))
            
        pu_dest = e, n
            
        validate = ", ".join([str(n1), str(n2)])
        
        enc_validate = rsa_encrypt(validate, pu_dest)
            
        client.send(enc_validate.encode())

        # last val
        enc_last_val = client.recv(1024).decode()
        last_val = rsa_decrypt(enc_last_val, private_key)
        print(f"7. N2: {last_val}")
        
        
        
    client.close()
    print("[INFO] Koneksi ditutup.")

if __name__ == "__main__":
    main()
