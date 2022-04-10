from datetime import datetime
import socket, threading

client_connections = []
max_connections = 2

def handle_connection(connection: socket.socket, address: str) -> None:
    
    while True:
        try:
            client_message = connection.recv(1024)
            client_message_at = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

            if client_message:
                client_message_decode = client_message.decode()
                message_meta = client_message_decode.split(";")

                print(f"Message from [{address[0]}:{address[1]}][{message_meta[1]}] at [{client_message_at}] : {message_meta[0]}")

                message_to_broadcast = f"[{client_message_at}] {message_meta[1]} : {message_meta[0]}"
                broadcast_message(message_to_broadcast, connection)

            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f"Error : {e}")
            remove_connection(connection)
            break

def remove_connection(conn: socket.socket) -> None:

    if client_connection in client_connections:
        client_connection.close()
        client_connections.remove(client_connection)

def broadcast_message(message: str, connection: socket.socket) -> None:
    
    for client_connection in client_connections:
        if client_connection != connection:
            try:
                client_connection.send(message.encode())

            except Exception as e:
                print(f"Error : {e}")
                remove_connection(client_connection)

def server() -> None:
    
    listening_port = 12000

    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', listening_port))
        socket_instance.listen(max_connections)

        print('[ +++ Server running +++ ]')

        while True:
            socket_connection, address = socket_instance.accept()
            client_connections.append(socket_connection)
            threading.Thread(target=handle_connection, args=[socket_connection, address]).start()
    
    except Exception as e:
        print(f"Error : {e}")
    
    finally:
        if len(client_connections) > 0:
            for client_connection in client_connections:
                remove_connection(client_connection)

        socket_instance.close()

if __name__ == "__main__":
    server()