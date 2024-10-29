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

numOfTurns = 0

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)

    message = TTTserver.Message(sel, conn, addr, (len(clients)+1))

    player = PlayerData((len(clients)+1), "Test", addr, message)
    clients.append(player)

    sel.register(conn, selectors.EVENT_READ, data=message)


def service_connection(key, mask):

    message = key.data

    #If not all players connected yet
    global playersConnected
    if(not playersConnected):
        print("not all players")
        message.process_events(mask)

        if(len(clients) == 2):
            playersConnected = True
            clients[0].Message.write("Name", "")
            clients[1].Message.write("Name", "")

        return
    
    #If a move has been made, inform other client
    message.process_events(mask)
    global numOfTurns
    if(message.action=="Move"):
        numOfTurns += 1

        if(numOfTurns >= 2):
            for c in clients:
                c.Message.write("End", "End of Game, Goodbye.")
                c.Message.close()
                #sel.unregister(c.Message.sock)
            sel.close()
            exit()

        #If player 1 made a move
        if(message.ID == 1):
            print("Test1")
            clients[1].Message.write("Your_Turn", "Player 2, It is your Turn.")
        #If player 2 made a move
        else:
            print("Test2")
            clients[0].Message.write("Your_Turn", "Player 1, It is your Turn.")

    return


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)
    

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
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