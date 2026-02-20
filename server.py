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


try:
    while True:
        # Wait for message from client (blocks until data arrives)
        data = client_socket.recv(1024)
        

        # If empty bytes returned, client disconnected
        if not data:
            print(f"[DISCONNECTED] {addr}. Client disconnected.")
            break
        

        # Convert bytes -> string
        message = data.decode('utf-8')
        print("Client says:", message)
        

        # Send a reply back to the client (string -> bytes)
        reply = f"Server recieved: {message}"
        client_socket.send(reply.encode('utf-8'))


finally:
    client_socket.close()
    server_socket.close()
    print("Server closed")
