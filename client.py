import sys
import socket
import selectors
import traceback
import struct

import TTTclient

sel = selectors.DefaultSelector()

def create_request(action, move=""):
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, move=move),
    )

def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = TTTclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

def process_connection(key, mask):

    message = key.data

    message.process_events(mask)

    action = message.action

    if(action == "Your_Turn"):
         print(updated_board(message.board))
         move = input("Enter Move:\n")

         request = create_request("Move", move)
         message.request = request
         message.write()
         
    elif(action == "Name"):
         name = input("Enter a Username:\n")
         request = create_request("Name", name)
         message.request = request
         message.write()

    elif(action == "End"):
         message.close()
         exit()


    return

def updated_board(array):
     if(len(array) < 1):
          array = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
     board = f"\n    1   2   3\n  +-----------+\nA | {array[0]} | {array[1]} | {array[2]} |\n  +-----------+\nB | {array[3]} | {array[4]} | {array[5]} |\n  +-----------+\nC | {array[6]} | {array[7]} | {array[8]} |\n  +-----------+\n"
     return board

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action = "Connect"
request = create_request(action)
start_connection(host, port, request)

while True:
    events = sel.select(timeout=1)
    for key, mask in events:
        try:
            process_connection(key, mask)
        except Exception:
            print("Error, disconnecting.")
            exit()