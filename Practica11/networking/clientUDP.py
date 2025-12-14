import socket


class ClientUDP:
    def __init__(self, port: int = 0) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((socket.gethostbyname(socket.gethostname()), port))
        self.LOCAL_IP, self.CLIENT_PORT = self.sock.getsockname()

    def listen(self) -> dict[str, str]:
        data, address = self.sock.recvfrom(256)
        return {
            "data": data.decode(),
            "address": address
        }

    def send_to(self, data: str, target_ip: str, target_port: int) -> None:
        self.sock.sendto(data.encode(), (target_ip, target_port))


if __name__ == "__main__":
    client = ClientUDP()
    for i in range(100):
        client.send_to(
            data="Hola Rafa",
            target_ip="158.42.206.176",
            target_port=13000
        )

    # client.listen()
