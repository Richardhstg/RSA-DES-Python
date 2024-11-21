import socket
import threading

# List untuk menyimpan koneksi klien
clients = []

def broadcast(message, sender_socket):
    """Meneruskan pesan ke semua klien kecuali pengirim."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, address):
    """Fungsi untuk menangani komunikasi dengan klien tertentu."""
    print(f"[INFO] Koneksi diterima dari {address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"[{address}] {message.decode()}")
            broadcast(message, client_socket)
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