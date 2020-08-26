import sys
import select
from socket import socket, AF_INET, SOCK_STREAM

# invalid arguments
if len(sys.argv) < 3:
    print("Invalid inputs. Please stick to the format shown below.")
    print("$ python3 client.py <portnumber> <username>")
    print("portnumber: the port of the chatroom server.")
    print("username:   your alias used instead of IP/port combination.")
    sys.exit(0)

# define server address
SERVER_PORT = int(sys.argv[1])
SERVER_NAME = '127.0.0.1'

USERNAME = sys.argv[2]

# create TCP connection
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_NAME, SERVER_PORT))

# send username before broadcasting begins
client_socket.send(USERNAME.encode())
print("You have entered the chat!")
print("Send 'bye' to stop chatting.", end="\n\n")

while True:
    try:
        # the input 'select' code is inspired from
        # https://www.geeksforgeeks.org/simple-chat-room-using-python/
        # lines 35-36, 49, 59-60

        # select which medium of input
        sockets_list = [sys.stdin, client_socket]
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for input_src in read_sockets:
            if input_src == client_socket:
                message: str = client_socket.recv(2048).decode()
                print(message)

                if message == "__SERVER_ERROR__":
                    client_socket.close()
                    sys.stdout.flush()
                    sys.exit(0)

            else:
                message = sys.stdin.readline()

                client_socket.send(message.encode())

                # terminate the client-side connection
                if message == "bye\n":
                    client_socket.close()
                    sys.stdout.flush()
                    sys.exit(0)

                sys.stdout.write('\n')
                sys.stdout.flush()

    except KeyboardInterrupt:
        client_socket.send("bye\n".encode())
        client_socket.close()
        sys.stdout.flush()
        sys.exit(0)
