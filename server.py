# this python file handles the connection to the servers
import socket
from objects.game_objects import Player
from _thread import *
import pickle

server = "192.168.178.24"
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

# pre create two player objects one in red and the other one in blue
players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(connection, player):

    print(player)

    # using the the player id to get the Player object form the pre defined Player list
    connection.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            # 2048 bits is the amount of information we wait to recv. However, with errors you can try to increase the
            # size (e.g. 2048*8). But keep in mind that in increased size will also increase the waiting time
            data = pickle.loads(connection.recv(2048))
            players[player] = data

            if not data:
                # break the loop in case missing data
                print("Disconnected")
                break
            else:
                # we send the player position. If we are player 1 we send pos[0] otherwise we send pos[1]
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                # print status updates
                print("Received:", data)
                print("Sending:", reply)

            # encode replay into a bite object
            connection.sendall(pickle.dumps(reply))

        except Exception as err:
            print(err)
            break

    print("Lost connection")
    connection.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    # start thread and add the player to it as well
    start_new_thread(threaded_client, (conn, current_player))

    # add new player to the player counter
    current_player += 1
