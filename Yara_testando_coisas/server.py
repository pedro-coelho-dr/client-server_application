import socket
from models import Header, Packet  
import struct

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)

    print("HOST - waiting for a connection")

    while True:
        client_socket, client_address = server_socket.accept()

        print(f"HOST - connection from {client_address}")

        # Handshake: servidor envia mensagem de boas-vindas
        client_socket.sendall(b"Welcome to the server!")

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            # Decodifique a mensagem recebida em um objeto Packet
            packet = Packet(id=1, header=None, payload=None)
            packet_bytes = data

            # Extraia o cabeçalho e a carga útil da mensagem
            header_length = struct.calcsize('!H?')
            header_data = packet_bytes[:header_length]
            payload_data = packet_bytes[header_length:]

            # Decodifique o cabeçalho
            header_id, header_timer = struct.unpack('!H?', header_data)
            header = Header(id=header_id, timer=header_timer, unity="seconds")
            packet.header = header
            packet.payload = payload_data.decode('utf-8')

            print(f"HOST - received message with header ID: {header_id}, timer: {header_timer}, payload: {packet.payload}")

            
            if packet.payload == "2":
                print("\nClosing connection...")
                client_socket.close()
                server_socket.close()
                return

            # Mandando mensagem de confirmação do recebimento da mensagem do cliente
            client_socket.sendall(b"Message received - Capivara")

if __name__ == "__main__":
    server()
