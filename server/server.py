import socket

def send(client_connection, data):
    client_connection.sendall(data.encode())

def listening(client_connection):
    while True:
        #AQUI DEVE ESTRUTURAR O PACOTE RECEBIDO DO CLIENTE
        data = client_connection.recv(1024).decode()
        if data:
            print(f"\n{data}\n")
            send(client_connection, "ACK")
        else:
            print("[DISCONNECTED BY CLIENT]\n\n")
            break

def handshake(client_connection):
    attempts = 0
    max_attempts = 3
    try:
        syn = client_connection.recv(1024).decode()
        if syn == "SYN":
            while attempts < max_attempts:
                client_connection.sendall("SYN-ACK".encode())
                client_connection.settimeout(1.0)
                try:
                    ack = client_connection.recv(1024).decode()
                    if ack == "ACK":
                        print("[HANDSHAKE COMPLETE]")
                        client_connection.settimeout(None)
                        return True
                    else:
                        print("[INVALID ACK HANDSHAKE] Closing connection...")
                        return False
                except socket.timeout:
                    print("[NO ACK HANDSHAKE] Retrying...")
                    attempts += 1
                finally:
                    client_connection.settimeout(None)
            print("[HANDSHAKE FAILED] Closing connection...")
            return False
        else:
            print("[INVALID SYN HANDSHAKE] Closing connection...")
            return False
    except socket.timeout:
        print("[NO INITIAL HANDSHAKE] Closing connection...")
        return False

def start_server(host='localhost', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[SERVER] {host}:{port}")

        while True:
            client_connection, client_address = server_socket.accept()
            print(f"[HANDSHAKE]")
            with client_connection:
                if handshake(client_connection):
                    print(f"[CONNECTED] {client_address}")
                    listening(client_connection)
                else:
                    client_connection.close()

if __name__ == "__main__":
    start_server()