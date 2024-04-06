import struct

class Header:
    def __init__(self, id: int, timer: bool, unity: str):
        self.id = id
        self.timer = timer
        self.unity = unity
        self.length = None
        self.checksum = None

    def set_length(self, length: int):  # Tamanho do pacote em bytes
        self.length = length

    def set_checksum(self, checksum):  # checksum do pacote
        self.checksum = checksum


class Packet: # metodos de um pacote
    
    def __init__(self, id:int, header:Header, payload:str):
        self.id = id
        self.header = header
        self.payload = payload
    
    def serialize_to_binary(self) -> bytes:  # Serializa o pacote para binário para cálculo do checksum
        header_binary = struct.pack('!H?', self.header.id, self.header.timer)
        payload_binary = self.payload.encode('utf-8')
        return header_binary + payload_binary
    
    def calculate_checksum(self) -> int:  # Calcula o checksum do pacote
        packet_binary = self.serialize_to_binary()
        checksum = sum(packet_binary) % 256  # Exemplo de cálculo simples de checksum
        self.header.set_checksum(checksum)
        return checksum
    
    def calculate_packet_size(self) -> int:  # Calcula o tamanho total do pacote (payload + header)
        return len(self.payload.encode('utf-8')) + self.header.length
    
    def set_packet_id(self, id:int):  # ID do pacote
        self.id = id