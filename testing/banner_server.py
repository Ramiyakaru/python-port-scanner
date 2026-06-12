import socket

HOST = "0.0.0.0"
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Listening on {PORT}")

while True:
    client, addr = server.accept()

    client.send(
        b"Custome Banner server v1.0\r\n"
    )

    client.close()