import socket
from dataclasses import dataclass

from networking import ServerUDP

from message import Message


@dataclass
class Client:
    id: str
    username: str
    ip: str
    port: int

    def send_message(self, server_socket: socket.socket, message: Message) -> None:
        # Sends the list of messages to the client via the server socket
        data = f"message<sp>{message.sender_username}<sp>{message.content}"
        server_socket.sendto(data.encode(), (self.ip, self.port))

    def update_users(self, server_socket: socket.socket, clients: list['Client']) -> None:
        # Sends the list of connected users to the client via the server socket
        data_users = "users"
        for client in clients:
            data_users += f"<sp>{client.username}"
        server_socket.sendto(data_users.encode(), (self.ip, self.port))


class ChatServer:
    def __init__(self):
        self.clients = []
        self.messages: list[Message] = []
        self.sock = ServerUDP(port=8000)

    def receive_message(self, message: Message):
        self.messages.append(message)

    def add_client(self, client):
        self.clients.append(client)
        for client in self.clients:
            client.update_users(self.sock.sock, [c for c in self.clients])

    def remove_client(self, client):
        self.clients.remove(client)
        for client in self.clients:
            client.update_users(self.sock.sock, [c for c in self.clients])

    def update_state(self, client) -> None:
        # This method broadcasts the current state of the app (connected clients and chat history)
        for message in self.messages:
            client.send_message(self.sock.sock, message)

        client.update_users(self.sock.sock, [c for c in self.clients])

    def parse_incomming_message(self, data: str, address: tuple[str, int]) -> None:
        parts = data.split("<sp>")
        command = parts[0]

        if command == "connect":
            username = parts[1]
            new_client = Client(
                id=str(len(self.clients) + 1),
                username=username,
                ip=address[0],
                port=address[1]
            )
            self.add_client(new_client)
            self.update_state(new_client)

        elif command == "message":
            sender_username = parts[1]
            content = parts[2]
            sender_client = next(
                (c for c in self.clients if c.username == sender_username), None)
            if sender_client:
                new_message = Message(
                    sender_id=sender_client.id,
                    sender_username=sender_username,
                    content=content
                )
                self.receive_message(new_message)
                for client in self.clients:
                    client.send_message(self.sock.sock, new_message)

        elif command == "disconnect":
            username = parts[1]
            client_to_remove = next(
                (c for c in self.clients if c.username == username), None)
            if client_to_remove:
                self.remove_client(client_to_remove)

    def main_loop(self):
        print(
            f"Chat server running on ip {self.sock.LOCAL_IP} and port {self.sock.PORT}...")
        while True:
            incoming = self.sock.listen()
            data = incoming["data"]
            address = incoming["address"]
            print(f"Received data from {address}: {data}")
            self.parse_incomming_message(data, address)


if __name__ == "__main__":
    server = ChatServer()
    server.main_loop()
