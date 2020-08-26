import sys
import select
from socket import socket, AF_INET, SOCK_STREAM

from curses_trial import ChatScreen

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

# the TCP handshake is initiated by client from the server_port
# but once connection is established on a random port by the server
# all further communication is conducted via that port until closed

chat_screen = ChatScreen()

while True:
    try:
        # select which medium of input to select: stdin or socket
        sockets_list = [sys.stdin, client_socket]
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for socks in read_sockets:
            if socks == client_socket:
                message: str = socks.recv(2048).decode()
                print(message, end='')

            else:
                message = sys.stdin.readline()

                client_socket.send(message.encode())

                # terminate the client-side connection
                if message == "bye\n":
                    client_socket.close()
                    sys.stdout.flush()
                    sys.exit(0)

                sys.stdout.write("You: ")
                sys.stdout.write(message)
                sys.stdout.flush()

    except KeyboardInterrupt:
        client_socket.send("bye\n".encode())
        client_socket.close()
        sys.stdout.flush()
        sys.exit(0)
