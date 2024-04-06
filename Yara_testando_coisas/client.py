import socket
from models import Header, Packet

class Client:
    def __init__(self, host='localhost', port=12345):
        self.HOST = host
        self.PORT = port

    def start(self):
        while True:
            print("\n[1] Send message")
            print("[2] Exit\n")
            choice = input(">>> ")

            if choice == '1':

                header = Header(id=1, timer=True, unity="seconds")
                

                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((self.HOST, self.PORT))

                # Handshake: cliente recebe mensagem de boas-vindas do servidor
                print(clientSocket.recv(1024).decode())

                data = input("\n[MESSAGE]\n>>> ")

                packet = Packet(id=1, header=header, payload=data)

                clientSocket.send(packet.serialize_to_binary())
                
                modifiedSentence = clientSocket.recv(1024)
                print('From Server: ', modifiedSentence.decode())
                clientSocket.close()

            elif choice == '2':
                print("\nClosing connection...")
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((self.HOST, self.PORT))
                
                packet = Packet(id=1, header=header, payload="2")
                clientSocket.send(packet.serialize_to_binary())

                clientSocket.close()
                break
            
            else:
                print("[INVALID CHOICE]")

if __name__ == "__main__":
    client = Client()
    client.start()