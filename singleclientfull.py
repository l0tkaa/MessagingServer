import socket
import threading
from datetime import datetime
from logger_config import setup_logger

logger = setup_logger("client")  # logs go to console + logs/client.log

def connect_to_server():
    logger.info("Client connecting...")
    logger.error("Client error example")

# logging.basicConfig(
#     level=logging.DEBUG,  # show DEBUG, INFO, WARNING, ERROR messages
#     format='[%(asctime)s] %(levelname)s: %(message)s',  # timestamp + level + message
#     datefmt='%H:%M:%S'  # optional: just show hour:minute:second
# )

HOST = '127.0.0.1'
PORT = 12345


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def receive_messages(sock):
    """
    Thread function to constantly listen for messages form the server. 
    Runs in the background while main thread handles user input.
    """
    logger.info("clientrecieve messages function")
    while True:
        try:
            data = sock.recv(1024) #blocking read


            # if not data:
            #     print(f"\n[{timestamp()}] Server: {data.decode()}")
            #     break
            if not data:
                print(f"/[{timestamp()}] Server6666 client disconnected.")
                break

            print(f"\n[{timestamp()}] Server client23333 discoennected.")
            print("From client1111: ", end ="", flush=True)


        except Exception as e:
            logger.error(f"Receive error: {e}")
            break


def main():
 
    """
    Entry point for the client. Connects to server and starts to receive the thread. Main thread handles sending messages."""

    logger.debug("Client starting...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        logger.debug("attempting to connect...")
        client_socket.connect((HOST, PORT))
        logger.info("Client connected to server.")

    except Exception as e:
        logger.error(f"Client connection failed: {e}")
        return
    
    recv_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )
    recv_thread.start()

    # main thread handles sending messages
    while True:
        message = input("You22222: ")
        if message.lower() in ("/quit", "exit"):
            print(f"[{timestamp()}] Exiting chat...")
            try:
                client_socket.send("Client has left the chat.".encode())
            except:
                pass
            break
        try:
            # send user input to server
            client_socket.send(message.encode())
        except Exception as e:
            logger.error(f"Send failed: {e}")
            break

    # clean up
    client_socket.close()
    logger.info("Connection closed.")


if __name__ == "__main__":
    main()
