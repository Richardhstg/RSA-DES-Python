import socket
import threading
from RSA import *
from DES import des_decryption, des_encryption
from key_generator import generate_keys

clients = []
clients_pu = []
pr_pka = (381233, 541279)


def response_pu(sender_socket):
    for pu_key in clients_pu:
        if pu_key["client_socket"] != sender_socket:
            pu_dst = pu_key["pu"]
            break
    
    for client in clients:
        if client == sender_socket:
            try:
                enc_pu_dst = rsa_encrypt(pu_dst, pr_pka)
                client.send(enc_pu_dst.encode())
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, address):
    """Fungsi untuk menangani komunikasi dengan klien tertentu."""
    print(f"[INFO] Koneksi diterima dari {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
                        
            if not message:
                break
            
            message = rsa_decrypt(message, pr_pka)
            
            if message == "1":
                response_pu(client_socket)
            
            clients_pu.append({"client_socket": client_socket, "pu": message})
            
            print(f"client address : {address}, public key : {message}")

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
