import socket

def make_pkt(data, sequence_number):
    checksum = sum(bytearray(data.encode() + str(sequence_number).encode())) % 256
    checksum_string = f"{checksum:04d}"
    return f"{data}:{sequence_number}:{checksum_string}"

def parse_pkt(packet):
    parts = packet.rsplit(':', 2)
    if len(parts) == 3:
        data, seqnum, rcv_checksum = parts
        seqnum = int(seqnum)
        rcv_checksum = int(rcv_checksum)
        return data, seqnum, rcv_checksum
    else:
        raise ValueError("\n[PARSE ERROR] Invalid packet format")

def verify_checksum(data, sequence_number, rcv_checksum):
    checksum = sum(bytearray(data.encode() + str(sequence_number).encode())) % 256
    print(f"[CHECKSUM] {checksum} == {rcv_checksum}")
    return checksum == rcv_checksum

def isNAK(client_socket, data, sequence_number):
    print("[RESENDING]")
    send(client_socket, data, sequence_number)

def isACK(client_socket, sequence_number):
    try:
        client_socket.settimeout(1.0)
        packet = client_socket.recv(1024).decode()
        if packet:
            response, rcv_seq_num, rcv_checksum = parse_pkt(packet)
            if verify_checksum(response, rcv_seq_num, rcv_checksum):
                if response == "ACK" and rcv_seq_num == sequence_number:
                    print("\n[ACK received]")
                    return True
                elif response == "NAK":
                    print("\n[NAK received]")
                    return False
            else:
                print("\n[CHECKSUM ERROR] Data corrupted")
                return False
        else:
            print("[NO RESPONSE FROM SERVER]")
            return False
    except socket.timeout:
        print("[TIMEOUT] waiting ACK or NAK.")
        return False
    except ConnectionAbortedError as e:
        print("[CONNECTION ABORTED] Connection was aborted by the host.")
        return False

def send(client_socket, data, sequence_number):
    packet = make_pkt(data, sequence_number)
    client_socket.sendall(packet.encode())

def interface(client_socket):
    sequence_number = 0
    while True:
        print("\n[1] Send message")
        print("[2] Exit\n")
        choice = input(">>> ")
        if choice == '1':
            data = input("\n[MESSAGE]\n>>> ")
            send(client_socket, data, sequence_number)
            sequence_number += 1
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
