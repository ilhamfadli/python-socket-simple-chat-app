import socket, threading

name = "Client II"

def handle_message(connection: socket.socket):

    while True:
        try:
            message = connection.recv(1024)

            if message:
                print(message.decode())

            else:
                connection.close()

        except Exception as e:
            print(f"Error : {e}")
            connection.close()
            break

def client() -> None:

    server_address = "127.0.0.1"
    server_port = 12000

    try:
        socket_instance = socket.socket()
        socket_instance.connect((server_address, server_port))
        threading.Thread(target=handle_message, args=[socket_instance]).start()

        print("[ +++ Connected to chat room +++]")

        while True:
            message = input()

            message = message + f";{name}"

            if message == "quit":
                break

            socket_instance.send(message.encode())

        socket_instance.close()

    except Exception as e:
        print(f"Error : {e}")
        socket_instance.close()

if __name__ == "__main__":
    client()