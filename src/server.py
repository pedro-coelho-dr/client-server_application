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
    if len(packet) != 17:
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
                    if seqnum == last_seqnum:
                        print(f"[FULL MESSAGE] {full_message}")
                        full_message= ""
                else:
                    send_ack_nak(client_connection, "NAK", seqnum)
                    print(f"[ERROR] Checksum Seq: {seqnum}. NAK sent.")
                
            else:
                print("[DISCONNECTED] Client disconnected.")
                return
        
    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")



def listening_group(client_connection):
    try:
        full_message = "" #
        buffer = ""
        packets_to_ack = []
        temp_message = {}
        WINDOW_SIZE = 5
        expected_seqnum = 1
        

        while True:
            data = client_connection.recv(1024).decode()
            if not data:
                print("[DISCONNECTED] Client disconnected.")
                break
            buffer += data

            while len(buffer) >= 17:
                packet = buffer[:17] #cria o pacote
                buffer = buffer[17:] #remove o pacote do buffer
                
                try:
                    data, seqnum, last_seqnum, rcv_checksum = parse_pkt(packet)
                except ValueError as e:
                    print(f"[EXCEPTION] {str(e)}")
                    continue
                if seqnum != expected_seqnum:
                        print(f"[ERROR] PACKET LOSS. NAK sent.")
                        temp_message.clear()
                        packets_to_ack = []
                        expected_seqnum = (expected_seqnum - 1) // WINDOW_SIZE * WINDOW_SIZE + 1
                        buffer = ""
                        send_ack_nak(client_connection, "NAK", expected_seqnum)
                        break
                expected_seqnum += 1
             # CHECKSUM
                print(f"[RECEIVED] Data: '{data}', Last: {last_seqnum}, Seq: {seqnum}")
                if verify_checksum(data, seqnum, last_seqnum, rcv_checksum):
                    packets_to_ack.append((seqnum, True))
                    temp_message[seqnum] = data
                else:
                    packets_to_ack.append((seqnum, False))
                    print(f"[ERROR] Checksum Seq: {seqnum}. NAK.")
            # PONTO DE DECISÃO
                if len(packets_to_ack) == 5 or seqnum == last_seqnum:

                    if all(ack for _, ack in packets_to_ack):
                        send_ack_nak(client_connection, "ACK", packets_to_ack[-1][0])
                        print("[GROUP ACK SENT]")
                        for i in sorted(temp_message):
                            full_message += temp_message[i]
                        temp_message.clear()
                        if seqnum == last_seqnum:
                            print(f"\n[FULL MESSAGE] {full_message}")
                            full_message = ""
                            expected_seqnum = 1
                    else:
                        send_ack_nak(client_connection, "NAK", packets_to_ack[0][0])
                        print("[GROUP NAK SENT]")
                        temp_message.clear()
                        expected_seqnum = (packets_to_ack[0][0] - 1) // WINDOW_SIZE * WINDOW_SIZE + 1
                    packets_to_ack = []


    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")

# INTERFACE


def server_interface(client_connection):
    menu = """
[1] Packet Individual Confirmation
[2] Packet Group Confirmation
    """
    while True:
        print(menu)
        choice = input("Choose an option:\n>>> ")
        if choice == '1':
            if not listening(client_connection):
                break
        elif choice == '2':
            if not listening_group(client_connection):
                break
        else:
            print("[INVALID OPTION]")

# CONNECTION

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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[SERVER] {host}:{port}")

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            print(f"[CONNECTED] {client_address}")
            with client_connection:
                if handshake(client_connection):
                    server_interface(client_connection)
                else:
                    print("[HANDSHAKE FAILED] Connection closed.")
                    client_connection.close()
    except KeyboardInterrupt:
        print("[SERVER] Server closing...")
    except Exception as e:
        print(f"[ERROR] A {e}")
    finally:
        server_socket.close()
        print("[SERVER] Socket closed")

if __name__ == "__main__":
    start_server()