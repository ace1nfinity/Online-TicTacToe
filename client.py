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

    print("State: ", action)

    if(action == "Your_Turn"):
         print(updated_board())
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

def updated_board():
     board = "==============\nBoard Place-holder\n=============="
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
            process_connection(key, mask)
            #except Exception:
                #print(
                   # "main: error: exception for",
                    #f"{message.addr}:\n{traceback.format_exc()}",
                #)
                #message.close()
        # Check for a socket being monitored to continue.
        #if not sel.get_map():
            #break
#except KeyboardInterrupt:
    #print("caught keyboard interrupt, exiting")
#finally:
    #sel.close()