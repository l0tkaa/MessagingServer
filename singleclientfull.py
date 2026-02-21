import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

def receive_messages(sock):
    """
    Thread function to constantly listen for messages form the server. 
    Runs in the background while main thread handles user input.
    """
    while True:
        try:
            data = sock.recv(1024) #blocking read
            if not data:
                print(f"\n[{timestamp()}] Server: {data.decode()}")
                print("You: ", end="", flush=True)
        except Exception as e:
            print(f"\n[{timestamp()}] Receive error:", e)
            break
    
def main():
    """
    Entry point for the client. Connects to server and starts to receive the thread. Main thread handles sending messages."""

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"[{timestamp()}] Connected to server!")
    except Exception as e:
        print(f"[{timestamp()}] Connection failed:", e)
        return
    
    recv_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )
    recv_thread.start()

    # main thread handles sending messages
    while True:
        message = input("You: ")
        if message.lower() in ("/quit", "exit"):
            print(f"[{timestamp()}] Exiting chat...")
            try:
                client_socket.send("Client has left the chat.".encode())
            except:
                pass
            break
        try:
            #send user input to server
            client_socket.send(message.encode())
        except Exception as e:
            print(f"[{timestamp()}] Send failed: ", e )
            break
        
        #clean up
        client_socket.close()
        print(f"[{timestamp()}] Connection closed.") 

    if __name__ == "__main__":
        main()


