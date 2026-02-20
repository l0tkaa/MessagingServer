import socket
#receive and reply

# Bind to localhost on port 12345
HOST = '127.0.0.1'
PORT = 12345


#Create TCP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the created socket to localhost:12345 so clients know where to connect
server_socket.bind((HOST, PORT))
# Listen for incoming connections (queue up to 5 pending clients)
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")



# accept() blocks until a client connects
client_socket, addr = server_socket.accept()
print(f"Client connected from {addr}")



while True:
    data = client_socket.recv(1024) #wait for message
    if not data:
        print("Client disconnected")
        break
    message = input("You: ")
    client_socket.send(message.encode())

client_socket.close()
server_socket.close()