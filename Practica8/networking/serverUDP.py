import socket


class ServerUDP:
    def __init__(self, port: int) -> None:
        self.LOCAL_IP = socket.gethostbyname(socket.gethostname())
        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.LOCAL_IP, self.PORT))

    def listen(self) -> dict[str, str]:
        data, address = self.sock.recvfrom(256)
        return {
            "data": data.decode(),
            "address": address
        }

    def send_to(self, data: str, ip: str, port: int) -> None:
        self.sock.sendto(data.encode(), (ip, port))


if __name__ == "__main__":
    server = ServerUDP(port=8000)
    server.send_to(
        data="Hello World!",
        ip=server.LOCAL_IP,
        port=59456
    )
