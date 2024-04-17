import socket

# ACK NAK
def make_pkt(data, sequence_number):
    sequence_string = f"{sequence_number:04d}"
    checksum = sum(bytearray((data + sequence_string).encode())) % 256
    checksum_string = f"{checksum:04d}"
    return f"{data}{sequence_string}{checksum_string}"

def send_ack_nak(client_connection, ack_nak, sequence_number):
    packet = make_pkt(ack_nak, sequence_number)
    client_connection.sendall(packet.encode())
    print(f"[SENT] {ack_nak} for Seq: {sequence_number}\n\n")

# LISTENING

def parse_pkt(packet):
    if len(packet) < 12:
        raise ValueError("[PARSE ERROR]")
    data = packet[:-12]
    seqnum = int(packet[-12:-8])
    last_seqnum = int(packet[-8:-4])
    rcv_checksum = int(packet[-4:])
    return data, seqnum, last_seqnum, rcv_checksum

def verify_checksum(data, sequence_number, last_sequence_number, rcv_checksum):
    sequence_string = f"{sequence_number:04d}"
    last_seq_string = f"{last_sequence_number:04d}"
    checksum = sum(bytearray((data + sequence_string + last_seq_string).encode())) % 256
    print(f"[CHECKSUM] {checksum} == {rcv_checksum}")
    return checksum == rcv_checksum

def listening(client_connection):
    try:
        full_message = ""
        while True:
            packet = client_connection.recv(1024).decode()
            if packet:
                data, seqnum, last_seqnum, rcv_checksum = parse_pkt(packet)
                print(f"[RECEIVED] Data: '{data}', Last: {last_seqnum}, Seq: {seqnum}")
                if verify_checksum(data, seqnum, last_seqnum, rcv_checksum):
                    full_message += data
                    send_ack_nak(client_connection, "ACK", seqnum)
                else:
                    send_ack_nak(client_connection, "NAK", seqnum)
                    print(f"[ERROR] Checksum mismatch for Seq: {seqnum}. NAK sent.")
                if seqnum == last_seqnum:
                    print(f"[FULL MESSAGE] {full_message}")
                    full_message= ""
            else:
                print("[DISCONNECTED] Client has disconnected.")
                return
    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")

def listening_group(client_connection):
    return

def server_interface(client_connection):
    menu = """
1) Individual Packet Confirmation
2) Group Packet Confirmation
3) Exit
    """
    while True:
        print(menu)
        choice = input("Choose an option:\n>>> ")
        if choice == '1':
            listening(client_connection)
        elif choice == '2':
            listening_group(client_connection)
        elif choice == '3':
            print("[EXITING] Closing connection...")
            client_connection.close()
            break
        else:
            print("[INVALID OPTION] Please try again.")


### CONNECTION

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
            with client_connection:
                if handshake(client_connection):
                    print(f"[CONNECTED] {client_address}\n\n")
                    server_interface(client_connection)
                else:
                    client_connection.close()

if __name__ == "__main__":
    start_server()