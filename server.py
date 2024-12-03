import sys
import socket
import selectors
import traceback
import ipaddress
from typing import NamedTuple

import TTTserver
import GameManager

class PlayerData(NamedTuple):
    ID: int
    Name: str
    Address: str
    Message: TTTserver.Message

sel = selectors.DefaultSelector()

gameManager = GameManager.GameManager()

clients = []

playersConnected = False
namesCollected = False

currentPlayerTurn = 0
numOfTurns = 0

def accept_wrapper(sock):
    if(len(clients) >= 2):
        return
    
    conn, addr = sock.accept()  # Should be ready to read
    ServerLog(f"Accepted connection from {addr}.")
    conn.setblocking(False)

    message = TTTserver.Message(sel, conn, addr, (len(clients)+1), gameManager)

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

        global gameManager
        #Attempt to place received move, if a bad move let current player re-attempt move
        if(gameManager.PlaceMove(message.last_data, message.ID) == False and currentPlayerTurn == message.ID):
            ServerLog(f"Error in received move. Allowing Player {message.ID} to retry.")
            if(currentPlayerTurn == 1 and message.ID == 1):
                clients[0].Message.write("Move", f"Invalid Move, try Again. Enter a move in this format: <row><column> Ex: A1 | You are 'o'")
            #If player 2 made a move
            elif((currentPlayerTurn == 2 and message.ID == 2)):
                clients[1].Message.write("Move", f"Invalid Move, try Again. Enter a move in this format: <row><column> Ex: A1 | You are 'x'")
        else:
            #Check for Win before allowing another move to be made
            if(gameManager.CheckForWin()):
                EndGame(message.ID)
            elif(numOfTurns >= 9):
                EndGame(4)
            #If player 1 made a move
            if(currentPlayerTurn == 1 and message.ID == 1):
                numOfTurns += 1
                currentPlayerTurn = 2
                clients[1].Message.write("Move", f"{clients[1].Name}, It is your Turn. Enter a move in this format: <row><column> Ex: A1 | You are 'x'")
                ServerLog(f"Player {message.ID} has made move, changing to other Player.")
            #If player 2 made a move
            elif((currentPlayerTurn == 2 and message.ID == 2)):
                numOfTurns += 1
                currentPlayerTurn = 1
                clients[0].Message.write("Move", f"{clients[0].Name}, It is your Turn. Enter a move in this format: <row><column> Ex: A1 | You are 'o'")
                ServerLog(f"Player {message.ID} has made move, changing to other Player.")
            print(numOfTurns)
            

    elif(message.action=="Name"):
        if(message.ID == 1 and namesCollected == False):
            clients[0] = clients[0]._replace(Name = message.last_data)
        elif(message.ID == 2 and namesCollected == False):
            clients[1] = clients[1]._replace(Name = message.last_data)

        if (clients[0].Name != "_name_" and clients[1].Name != "_name_" and namesCollected == False):
            namesCollected = True
            currentPlayerTurn = 1
            ServerLog(f"All Players connected, beginning game.")
            clients[0].Message.write("Move", (f"{clients[0].Name}, It is your Turn. Enter a move in this format: <row><column> Ex: A1 | You are 'o'"))
            clients[1].Message.write("Move", "")

    return

def EndGame(endCode):


    output = "End of Game, Goodbye."

    if(endCode == 0):
        output = f"Other Player disconnected, ending game."
    elif(endCode == 1 and currentPlayerTurn == 1):
        output = f"{clients[0].Name} won!. Come play again! Goodbye."
        ServerLog(f"Player {clients[0].ID} won, ending game.")
    elif(endCode == 2 and currentPlayerTurn == 2):
        output = f"{clients[1].Name} won!. Come play again! Goodbye."
        ServerLog(f"Player {clients[1].ID} won, ending game.")
    elif(endCode == 4):
        output = f"It's a draw! End of Game, Goodbye."
        ServerLog(f"It was a draw, ending game.")


    try:
        clients[0].Message.write("End", output)
        clients[0].Message.close()
    except Exception:
        ServerLog(f"Disconnecting other client.")

    try:
        clients[1].Message.write("End", output)
        clients[1].Message.close()
    except Exception:
        ServerLog(f"Disconnecting other client.")

    sel.close()
    exit()
    return

def ServerLog(message):
    print(message)
    with open("server_log.txt", "a") as f:
                print(message, file=f)


if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<port>")
    sys.exit(1)

f = open('server_log.txt', 'r+')
f.truncate(0)

host = '0.0.0.0'
port = sys.argv[1]
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, int(port)))
lsock.listen()
ServerLog(f"listening on: {host}, {port}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            try:
                service_connection(key, mask)
            except Exception:
                ServerLog(f"Client pre-maturely disconnected, ending game. {Exception}")
                EndGame(0)
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