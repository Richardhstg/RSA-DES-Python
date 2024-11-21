import socket
import threading
from RSA import *
from DES import des_decryption, des_encryption
from key_generator import generate_keys

clients = []
clients_pu = []
pr_pka = (381233, 541279)

def forward(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

def response_pu(request_id, sender_socket):
    request_id = int(request_id)
    pu_dst = ""
    for pu_key in clients_pu:
        if pu_key["client_id"] == request_id:
            pu_dst = pu_key["pu"]
    
    if pu_dst == "":
        print("not found")
    
    for client in clients:
        if client == sender_socket:
            enc_pu_dst = rsa_encrypt(pu_dst, pr_pka)
            client.send(enc_pu_dst.encode())
            

def handle_client(client_socket, address):
    """Fungsi untuk menangani komunikasi dengan klien tertentu."""
    print(f"[INFO] Koneksi diterima dari {address}")
    while True:
        try:
            print("kembali ke sini")
            message = client_socket.recv(1024).decode()
                        
            if not message:
                break
            
            message = rsa_decrypt(message, pr_pka)
            
            if message == "1":
                print("request public key")
                enc_request_id = client_socket.recv(1024).decode()
                request_id = rsa_decrypt(enc_request_id, pr_pka)
                
                response_pu(request_id, client_socket)
                
                print("masi di sini")
                
                enc_validate_request = client_socket.recv(1024).decode()
                
                forward(enc_validate_request, client_socket)
                
                continue                
            
            if message == "last_validation":
                print("last validation")
                
                enc_last_val_req = client_socket.recv(1024).decode()
                
                forward(enc_last_val_req, client_socket)
                
                continue
            
            split_msg = message.split(", ")
            client_id = int(split_msg[0])
            e = int(split_msg[1])
            n = int(split_msg[2])
            
            pu_client = ", ".join([str(e), str(n)])
            
            clients_pu.append({"client_id": client_id, "pu": pu_client})
            
            print(f"client id : {client_id}, public key : {message}")

        except ConnectionResetError:
            break
    print(f"[INFO] Koneksi dari {address} terputus.")
    clients.remove(client_socket)
    client_socket.close()

def main():
    host = socket.gethostname()
    port = 5000

    server = socket.socket()
    server.bind((host, port))
    
    server.listen(5)
    
    print("[INFO] Server berjalan dan menunggu koneksi...")

    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[INFO] Koneksi aktif: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
