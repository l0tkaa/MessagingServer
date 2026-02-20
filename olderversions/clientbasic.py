"""
Server starts → listens.
Client connects.
Server blocks on recv() → “Waiting to receive…”
Client sends "message1 test" → server receives and prints it.
Server asks for input → you type "server respond test".
Server sends that reply.
Server loops back and blocks again on recv() → “Waiting to receive…”

Only one side can talk at a time because:
Both sides use blocking input()
Both sides use blocking recv()
Real chat apps solve this with:
Threads
or async I/O
or event loops

You now understand:
TCP connections stay open after one message
recv() blocks until new data arrives
Both sides can deadlock if each waits at the same time
Real chat systems need concurrency to avoid this
Next logical step (still simple):
Make the client able to receive messages even while youre typing
That will be your first introduction to threading — the foundation for multi-user chat servers.
"""

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

