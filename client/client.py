import socket

# ACK-NAK

def parse_pkt(packet):
    if len(packet) < 8:
        raise ValueError("[PARSE ERROR]")
    data = packet[:-8]
    seqnum = int(packet[-8:-4])
    rcv_checksum = int(packet[-4:])
    return data, seqnum, rcv_checksum

def verify_checksum(data, sequence_number, rcv_checksum):
    sequence_string = f"{sequence_number:04d}"
    checksum = sum(bytearray((data + sequence_string).encode())) % 256
    print(f"[CHECKSUM] {checksum} == {rcv_checksum}")
    return checksum == rcv_checksum

def receive_ack_nak(client_socket, timeout=2.0):
    client_socket.settimeout(timeout)
    try:
        packet = client_socket.recv(1024).decode()
        if packet:
            data, seqnum, rcv_checksum = parse_pkt(packet)
            valid = verify_checksum(data, seqnum, rcv_checksum)
            if valid:
                print(f"[RECEIVED] Data: '{data}', Seq: {seqnum}, Valid checksum.")
                if data == "ACK":
                    return seqnum, "ACK"
                elif data == "NAK":
                    return seqnum, "NAK"
            else:
                print("[ERROR] Invalid checksum.")
    except socket.timeout:
        print("[TIMEOUT] No ACK or NAK")
    finally:
        client_socket.settimeout(None)
    return None, "NO RESPONSE"

# PACKET SEND

def make_pkt(data, sequence_number, last_sequence_number):
    sequence_string = f"{sequence_number:04d}"
    last_seq_string = f"{last_sequence_number:04d}"
    checksum = sum(bytearray((data + sequence_string + last_seq_string).encode())) % 256
    checksum_string = f"{checksum:04d}"
    return f"{data}{sequence_string}{last_seq_string}{checksum_string}"


def send(client_socket, data, sequence_number, last_sequence_number):
    packet = make_pkt(data, sequence_number, last_sequence_number)
    client_socket.sendall(packet.encode())
    print(f"\n[SENT] Data: '{data}', Seq: {sequence_number}, Last: {last_sequence_number}")


def send_batch(client_socket):
    sequence_number = 1
    data = input("\nEnter data: ")
    packets = [data[i:i+5] for i in range(0, len(data), 5)]
    last_sequence_number = len(packets)
    MAX_RETRIES = 3
    for packet in packets:
        retries = 0
        send(client_socket, packet, sequence_number, last_sequence_number)
        _, response = receive_ack_nak(client_socket)

        while response != "ACK" and retries < MAX_RETRIES:
            if response == "NAK":
                print(f"[NAK RECEIVED] Resending Packet Sequence: {sequence_number}")
            else:
                print(f"[RESENDING] Packet Sequence: {sequence_number}, Attempt: {retries+1}")
            
            send(client_socket, packet, sequence_number, last_sequence_number)
            _, response = receive_ack_nak(client_socket)
            retries += 1

        if retries == MAX_RETRIES and response != "ACK":
            print(f"[ERROR] Maximum resend: {sequence_number}.")
        sequence_number += 1



def send_batch_group(client_socket):
    return


## INTERFACE

def interface(client_socket):
    menu = """
1) Send batch (individual confirmation)
2) Send batch (group confirmation)
3) Exit
    """
    while True:
        print(menu)
        choice = input("Choose an option:\n>>> ")
        if choice == '1':
            send_batch(client_socket)
        if choice == '2':
            send_batch_group(client_socket)
        elif choice == '':
            print("[EXITING] Closing connection...")
            client_socket.close()
            break
        else:
            print("[INVALID OPTION] Please try again.")


#### CONNECTIONG

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
            print("[CONNECTION FAILED] Handshake unsuccessful.")
            client_socket.close()

if __name__ == "__main__":
    connection()