import socket
import time


def start_client(key):
    server_ip = "192.168.253.131"
    server_port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to server")

        # while True:
        message = "Alive"
        client_socket.sendall(message.encode())
        print(f"Sent: {message}")
        response = client_socket.recv(1024).decode()
        print(f"Received: {response}")

        # Send the key first and then ensure that client is alive
        client_socket.sendall("key:".encode())
        client_socket.sendall(key)
        print(f"sent: Key: {key}")
        response = client_socket.recv(1024).decode()
        print(f"Received: {response}")
        # time.sleep(20)  # keep connection alive
    except KeyboardInterrupt:
        print("Client exiting")
    finally:
        client_socket.close()

# if __name__ == "__main__":
#     start_client()
