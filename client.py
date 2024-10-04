import sys
import socket
import selectors

sel = selectors.DefaultSelector()

def create_request(action, value):
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, value=value),
    )

def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    #message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=None)

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    #message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=None)

host, port = sys.argv[1], int(sys.argv[2])
action, value = 10, 20
request = create_request(action, value)
start_connection(host, port, request)