"""
In this, you're introducing:
Concurrent I/O
Background network listeners
Continuous open TCP connections
Real-time message reception
This is the conceptual foundation behind:
Discord clients
Slack desktop app
Multiplayer game clients
All of them maintain a persistent socket and a background receive loop.

Expected Behavior Now
Run server
Run client
Type on client → server receives
Type on server → client prints instantly (even if you’re mid-typing)
That “instant message appearing while typing” is the first time your program feels like a real messaging system.
"""

import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    """this runs in a separate thread. 
    it constantly listens for messages from the server"""

    while True:
        try:
            data = sock.recv(1024) #blocks until user sends data
            if not data:
                print("\n[CLIENT] Server disconnected.")
                break
            
            print(f"\nServer: {data.decode()}")
            print("You: ", end="", flush=True)

        except Exception as e:
            print("\n[CLIENT] Error receiving:", e)
            break
        

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print("[CLIENT] Connected to server!")
    except Exception as e:
        print("[CLIENT] Connection failed:", e)
        return
    
    receiver_thread = threading.Thread(
        target = receive_messages, 
        args = (client_socket,),
        daemon=True # dies when main thread exits
    )
    receiver_thread.start()

    # Main thread handles user input and sending messages
    while True:
        message = input("You: ")
        try:
            client_socket.send(message.encode())
        except Exception as e:
            print("[CLIENT] Send failed:", e)
            break
        
    client_socket.close()

if __name__ == "__main__":
    main()
