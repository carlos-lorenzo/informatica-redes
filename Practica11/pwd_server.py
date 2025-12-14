from networking import ServerUDP

CREDENTIALS = {
    "lorenzo": "123"
}

pwd_server = ServerUDP(port=8080)
print(f"Server running on {pwd_server.LOCAL_IP}:{pwd_server.PORT}")

while True:
    message = pwd_server.listen()
    username, password = message.get("data", {}).split(":")
    address = message.get("address")
    client_ip = address[0]
    client_port = address[1]
    message_sent = ""
    if password == CREDENTIALS.get(username):
        message_sent = f"{username}:OK"

    else:
        message_sent = f"{username}:ERR"

    pwd_server.send_to(message_sent, client_ip, client_port)
    print(f"Sent {message_sent} to {client_ip}:{client_port}")
