import socket

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
    client_socket.connect((HOST, PORT))
    print(f"Connected to server{HOST}:{PORT}")
except ConnectionRefusedError:
    print(f"Connection failed! Make sure the server at {HOST}:{PORT} is running.")
    exit()   
    