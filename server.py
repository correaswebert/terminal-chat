import sys
import os
from datetime import datetime
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

    # alert peers about new connection
    for peer in peers:
        if peer != conn_socket:
            peer.send(f"{name} has joined the chat\n".encode())

    while True:
        # receive the message and broadcast it in the network
        msg: str = conn_socket.recv(1024).decode()
        time = datetime.now().strftime("%H:%M:%S")

        # broadcast the data to all peers in the network
        for peer in peers:
            if peer != conn_socket:
                timed_msg = f"[{time}] {name}\n" + msg
                peer.send(timed_msg.encode())

        # terminate server-side connection with user
        if msg == "bye\n":
            peers.remove(conn_socket)
            conn_socket.close()
            return


while True:
    try:
        # a new client request received on server_port
        # once accepted, a random port is assigned for further communication
        conn_socket, _ = server_socket.accept()

        peers.append(conn_socket)

        # create a thread and start its execution
        Thread(target=newUser, args=(conn_socket,)).start()

    except KeyboardInterrupt:
        # alert clients to close their connection
        for peer in peers:
            peer.send("__SERVER_ERROR__".encode())

        server_socket.close()
        print("Server has stopped listening.")

        # current process is stopped, any spawned threads are also killed
        os._exit(0)
