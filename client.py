import socket

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    client_socket.connect((HOST, PORT))
    print("[CLIENT] Connected to server!")
except Exception as e:
    print("[CLIENT] Connection failed:", e)
    exit()


while True:
    message = input("Input message here: ")
    print(f"[CLIENT] Sending: {message!r}")
    client_socket.send(message.encode('utf-8'))


    print("[CLIENT] Sending: {message!r}")
    data = client_socket.recv(1024)
    print(f"[CLIENT] Raw bytes received: {data!r}")


    if not data:
        print("[CLIENT] Server disconnected")
        break
    
    print("Server:", data.decode('utf-8'))
client_socket.close()

        
