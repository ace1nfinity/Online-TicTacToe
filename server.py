import sys
import socket
import selectors
import traceback
from typing import NamedTuple

import TTTserver

class PlayerData(NamedTuple):
    ID: int
    Name: str
    Address: str
    Message: TTTserver.Message

sel = selectors.DefaultSelector()

clients = []

playersConnected = False
namesCollected = False

currentPlayerTurn = 0
numOfTurns = 0

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    with open("server_log.txt", "a") as f:
        print("accepted connection from", addr, file=f)
    conn.setblocking(False)

    message = TTTserver.Message(sel, conn, addr, (len(clients)+1))

    player = PlayerData((len(clients)+1), "_name_", addr, message)
    clients.append(player)

    sel.register(conn, selectors.EVENT_READ, data=message)


def service_connection(key, mask):

    message = key.data

    #If not all players connected yet
    global playersConnected
    if(not playersConnected):
        message.process_events(mask)

        if(len(clients) == 2):
            playersConnected = True
            clients[0].Message.write("Name", "")
            clients[1].Message.write("Name", "")

        return
    
    #If a move has been made, inform other client
    message.process_events(mask)
    global namesCollected
    global currentPlayerTurn
    global numOfTurns
    if(message.action=="Move"):

        numOfTurns += 1

        if(numOfTurns >= 4):
            for c in clients:
                c.Message.write("End", "End of Game, Goodbye.")
                c.Message.close()
                #sel.unregister(c.Message.sock)
            sel.close()
            exit()
        else:
            #If player 1 made a move
            if(currentPlayerTurn == 1 and message.ID == 1):
                currentPlayerTurn = 2
                clients[1].Message.write("Move", f"{clients[1].Name}, It is your Turn.")
            #If player 2 made a move
            elif((currentPlayerTurn == 2 and message.ID == 2)):
                currentPlayerTurn = 1
                clients[0].Message.write("Move", f"{clients[0].Name}, It is your Turn.")

    elif(message.action=="Name"):
        if(message.ID == 1):
            clients[0] = clients[0]._replace(Name = message.last_data)
        else:
            clients[1] = clients[1]._replace(Name = message.last_data)

        if (clients[0].Name != "_name_" and clients[1].Name != "_name_" and namesCollected == False):
            namesCollected = True
            currentPlayerTurn = 1
            clients[0].Message.write("Move", (f"{clients[0].Name}, It is your Turn."))
            clients[1].Message.write("Move", "")

    return


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

f = open('server_log.txt', 'r+')
f.truncate(0)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
with open("server_log.txt", "a") as f:
    print("listening on", (host, port), file=f)
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
                #try:
                    #message.process_events(mask)
                #except Exception:
                    #print(
                        #"main: error: exception for",
                        #f"{message.addr}:\n{traceback.format_exc()}",
                    #)
                    #message.close()
#except KeyboardInterrupt:
    #print("caught keyboard interrupt, exiting")
#finally:
    #sel.close()