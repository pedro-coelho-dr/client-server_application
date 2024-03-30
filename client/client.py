import socket

def make_pkt(data):
    checksum = sum(bytearray(data.encode())) % 256
    checksum_string = f"{checksum:04d}"
    return f"{data}{checksum_string}"


def parse_pkt(packet):
    checksumlen = 4
    data = packet[:-checksumlen]
    checksum = int(packet[-checksumlen:])
    return data, checksum

def verify_checksum(data, rcv_checksum):
    checksum = sum(bytearray(data.encode())) % 256
    return checksum == rcv_checksum

def isNAK(client_socket, data):
    print("[RESENDING]")
    send(client_socket, data)

def isACK(client_socket):
    try:
        client_socket.settimeout(1.0)
        packet = client_socket.recv(1024).decode()
        response, rcv_checksum = parse_pkt(packet)
        if verify_checksum(response, rcv_checksum):
            if response == "ACK":
                print("\n[ACK received]")
                return True
            elif response == "NAK":
                print("\n[NAK received]")
                return False
        else:
            print("\n[CHECKSUM ERROR] Data corrupted")
            return False
    except socket.timeout:
        print("[TIMEOUT] waiting ACK or NAK.")
        return False

def send(client_socket, data):
    #AQUI DEVE ESTRUTURA O PACOTE ANTES DE ENVIAR PARA O SERVIDOR
    packet = make_pkt(data)
    client_socket.sendall(packet.encode())
    if not isACK(client_socket):
        isNAK(client_socket, data)

def interface(client_socket):
    while True:
        print("\n[1] Send message")
        print("[2] Exit\n")
        choice = input(">>> ")
        if choice == '1':
            data = input("\n[MESSAGE]\n>>> ")
            send(client_socket, data)
        elif choice == '2':
            print("\n[EXIT] Closing connection...")
            break
        else:
            print("[INVALID CHOICE]")

def handshake(client_socket):
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        client_socket.sendall("SYN".encode())
        try:
            client_socket.settimeout(1.0)
            syn_ack = client_socket.recv(1024).decode()
            if syn_ack == "SYN-ACK":
                client_socket.sendall("ACK".encode())
                print("[HANDSHAKE COMPLETE]")
                client_socket.settimeout(None)
                return True
            else:
                print("[INVALID SYN-ACK HANDSHAKE] Closing connection...")
                return False
        except socket.timeout:
            print("[NO SYN-ACK HANSHAKE] Retrying...")
            attempts += 1
        finally:
            client_socket.settimeout(None)
    print("[HANDSHAKE FAILED] Closing connection...")
    return False

def connection(server_host='localhost', server_port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))

        peer_address = client_socket.getpeername()
        local_address = client_socket.getsockname()
        if handshake(client_socket):
            print(f"[CONNECTED] {server_host}:{server_port} / {peer_address[0]}:{peer_address[1]} / {local_address[0]}:{local_address[1]}")
            interface(client_socket)
        else:
            client_socket.close()

if __name__ == "__main__":
    connection()