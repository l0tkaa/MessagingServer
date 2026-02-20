import socket
import threading

HOST = '127.0.0.1'
PORT = 12345


def receive_messages(client_socket):
    """
    Continuously receives messages from the client.
    Runs in its own thread so it never blocks on input().
    """


    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[SERVER] Client disconnected.")
                break
            print(f"\nClient: {data.decode()}")
            print("You: ", end="", flush = True)
        except Exception as e:
            print("\n[SERVER] Receive error:", e)
            break



def send_messages(client_socket):
    """
    Handles server-side user input without blocking recieve().
    """
    while True:
        try:
            message = input("You: ")
            client_socket.send(message.encode())
        except Exception as e:
            print("\n[SERVER] Send error:", e)
            break



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server listening on {HOST}:{PORT}...")

    client_socket, addr = server_socket.accept()
    print(f"Client connected to{addr}")

    recv_thread = threading.Thread(
        target = receive_messages,
        args = (client_socket,),
        daemon=True
    )


    recv_thread.start()


    send_messages(client_socket)


    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()