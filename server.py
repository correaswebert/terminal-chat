import sys
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

# invalid arguments
if len(sys.argv) < 2:
    print("Invalid inputs. Please stick to the format shown below.")
    print("$ python3 client.py <portnumber>")
    print("portnumber: the port of the chatroom server.")
    sys.exit(0)

# define server address
server_name = "127.0.0.1"
server_port = int(sys.argv[1])

# create a new TCP socket and bind it to server address
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_name, server_port))

# start listening on the bound port
server_socket.listen(1)
print(f"TCP server is listening on port {server_port}.")

peers = []


def newUser(conn_socket: socket):
    name: str = conn_socket.recv(1024).decode()
    # msg: str = ...

    while True:
        # receive the message and broadcast it in the network
        msg: str = conn_socket.recv(1024).decode()

        # time = datetime.now().strftime("%H:%M:%S")

        # broadcast the data to all peers in the network
        for peer in peers:
            if peer != conn_socket:
                peer.send(f"{name}: {msg}".encode())

        # terminate server-side connection with user
        if msg == "bye\n":
            # XXX: may need to apply mutex here
            peers.remove(conn_socket)

            conn_socket.close()

            print(f"{name} left the chat")
            return


while True:
    try:
        # a new client request received on server_port
        # once accepted, a random port is assigned for further communication
        conn_socket, _ = server_socket.accept()

        # XXX: may need to apply mutex here
        peers.append(conn_socket)

        # create a thread and start its execution
        Thread(target=newUser, args=(conn_socket,)).start()

    except KeyboardInterrupt:
        server_socket.close()
        print("Server has stopped listening.")
        break