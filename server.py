import socket


# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# HOST = '127.0.0.1'
# PORT = 12345
# server_socket.bind((HOST, PORT))

# server_socket.listen(1)

# #keep connection open until client disconnects
# try:
#     while True:
#         data = client_socket.recv(1024)
#         if not data:
#             break
# finally:
#     print("Connection closed")
#     client_socket.close()
#     server_socket.close()

#Create TCP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to localhost on port 12345
HOST = '127.0.0.1'
PORT = 12345
server_socket.bind((HOST, PORT))

# Listen for a single connection
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")

# Accept a connection (blocks until a client connects)
client_socket, client_address = server_socket.accept()
print(f"Client connected from {client_address}")

# Keep connection open until client disconnects
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

finally:
    print("Connection closed")
    client_socket.close()
    server_socket.close()
    