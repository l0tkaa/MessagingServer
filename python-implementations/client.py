# send messange, recieve reply

import socket

HOST = '127.0.0.1'
PORT = 12345

#create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    client_socket.connect((HOST, PORT))
except Exception as e:
    print("Connection failed:", e)
    exit()

# loop on both client and server
while True:
    #take user input
    message = input("Input message here: ")

    #send message to server (encode string -> bytes)
    client_socket.send(message.encode('utf-8'))

    #wait for server reply (blocks until server responds)
    data = client_socket.recv(1024)
    if not data:
        print("Server disconnected")
        break
    
    #decode bytes -> string and print
    print("Server:", data.decode('utf-8'))
client_socket.close()

# except ConnectionRefusedError:
#     print(f"Connection failed! Make sure the server at {HOST}:{PORT} is running.")

# finally:
#     client_socket.close()
#     print("Client closed")
        
