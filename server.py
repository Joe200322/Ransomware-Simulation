import socket

def start_server():
    server_ip = "192.168.253.131"
    server_port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Server listening on {server_ip}:{server_port}")

    while True:  # server NEVER stops

        conn, addr = server_socket.accept()
        print(f"Client connected: {addr}")

        try:
            while True:
                data = conn.recv(1024)

                if not data:
                    print(f"Client {addr} disconnected")
                    break  # stop handling THIS client only

                print(f"Received from {addr}: {data}")
                with open("key.txt",'ab') as f:
                    f.write(data)
                conn.sendall(b"ACK")
            

        except Exception as e:
            print(f"Client error: {e}")

        finally:
            conn.close()
            print(f"Connection with {addr} closed")

if __name__ == "__main__":
    start_server()
