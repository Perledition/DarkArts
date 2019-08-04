# this python file handles the connection to the servers
import socket
from _thread import *
import sys

server = ""
port = 5555

# creates the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try to connect put print the error in case port is not available
try:
    s.bind((server, port))
except socket.error as err:
    str(err)


# start to listen for connections
# only put 2 people in one connection
s.listen(2)
print("Waiting for a connection , Server Started")


def threaded_client(connection):

    reply = ""
    while True:
        try:
            # 2048 bits is the amount of information we wait to recv. However, with errors you can try to increase the
            # size (e.g. 2048*8). But keep in mind that in increased size will also increase the waiting time
            data = connection.recv(2048)
            reply = data.decode("utf-8")

            if not data:

                # break the loop in case missing data
                print("Disconnected")
                break
            else:

                # print status updates
                print("Received:", reply)
                print("Sending:", reply)

            # encode replay into a bite object
            conn.sendall(str.encode(reply))

        except Exception as err:
            print(err)
            break


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))