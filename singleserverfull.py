import socket
import threading
from datetime import datetime


# Server configuration
HOST = '127.0.0.1'
PORT = 12345

def timestamp():
    """
    Returns the current time formatted as HH:MM:SS.
    Used to tag messages for easier tracking.
    """

    return datetime.now().strftime("%H:%M:%S")

def receive_messages(client_socket):
    """
    Thread function to continuously listen for messages from the client. Runs in the background, allowing the main thread to handle sending. 
    """
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                # Client disconnected cleanly
                print(f"\n[{timestamp()}] Client disconnected.")
                break
            
            print(f"\n[{timestamp()}] Client: {data.decode()}" )
            print("You: ", end="", flush=True)
        except Exception as e:
            print(f"\n[{timestamp()}] Receive error:", e)
            break


def send_messages(client_socket):
    """
    Main thread function for server input and sending messages to client. Loops until server types '/quit' or client disconnects. 
    """
    while True:
        try:
            message = input("You: ")
            if message.lower() in ("/quit", "exit"):
                print(f"[{timestamp()}] Closing connection...")
                client_socket.send("Server has left the chat.".encode())
                break
            client_socket.send(message.encode())
        except Exception as e:
            print(f"\n[{timestamp()}] Send error:", e)
            break

def main():
    """
    Entry point for the server. 
    Sets up the socket, accepts a client, and starts threads for communication. 
    """

    # Create TCP socket (IPv4)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections (1 means max 1 queued connection)
    server_socket.listen(1)
    print(f"[{timestamp()}] Server listening on {HOST}:{PORT}...")

    client_socket, addr = server_socket.accept()
    print(f"[{timestamp()}] Client connected from {addr}")

    recv_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )

    recv_thread.start()

    send_messages(client_socket)

    client_socket.close()
    server_socket.close()
    print(f"[{timestamp()}] Server shutdown.")

if __name__ == "__main__":
    main()


