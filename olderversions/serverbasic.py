import socket

HOST = '127.0.0.1'
PORT = 12345


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")


client_socket, addr = server_socket.accept()
print(f"Client connected to {addr}")


while True:
    print("[SERVER] Waiting to receive...")
    data = client_socket.recv(1024) 
    print(f"[SERVER] Raw bytes received: {data!r}")

    if not data:
        print("[Server] Client disconnected")
        break
    
    decoded = data.decode()
    print("[SERVER] Client says:", decoded)

    message = input("You: ")
    client_socket.send(message.encode())


client_socket.close()
server_socket.close()

