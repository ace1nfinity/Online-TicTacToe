
import sys
import selectors
import json
import io
import struct

class Message:

    def __init__(self, selector, sock, addr, ID):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.ID = ID
        self.action = None
        self.last_data = None

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
                self._set_selector_events_mask("r")
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                #if sent and not self._send_buffer:
                    #self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _create_response(self, server_action, message = ""):
        self.action = self.request.get("action")
        self.last_data = self.request.get("move")
        if self.action == "Connect":

            if server_action == "Name":
                server_action = "Name"
                message = "Welcome to Tic-Tac-Toe!"

            elif self.ID == 1:
                server_action = "Waiting"
                message = "Welcome! Waiting for second Player to Connect..."

        elif self.action == "Name" and server_action!="Move":
            server_action = "Waiting"
            message = "Waiting for other Player..."

        
        elif self.action=="Move" or server_action=="Move":
            if(server_action == "End"):
                content = dict(action=server_action, message=message)
                content_encoding = "utf-8"
                response = {
                "content_bytes": self._json_encode(content, content_encoding),
                "content_type": "text/json",
                "content_encoding": content_encoding,
                }
                return response

            if(message != ""):
                server_action = "Your_Turn"
                message = message
            else:
                server_action = "Waiting"
                message = "Other Player's Turn. Waiting..."

        else:
            content = {"result": f'Error: invalid action "{self.action}".'}

        with open("server_log.txt", "a") as f:
                print(f"sending: Action '{server_action}', Message '{message}' to ", self.addr, file=f)

        content = dict(action=server_action, message=message)
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write("")

    def read(self):
        self.request = None
        self._recv_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None

        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self, action, message = ""):
        self._send_buffer = b""
        self.create_response(action, message)
        self._write()

    def close(self):
        with open("server_log.txt", "a") as f:
            print("closing connection to", self.addr, file=f)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            with open("server_log.txt", "a") as f:
                print(
                f"error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}", file=f,
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            with open("server_log.txt", "a") as f:
                print("received request", repr(self.request), "from", self.addr, file=f)
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self, action, message):
        response = self._create_response(action, message)
        message = self._create_message(**response)
        self._send_buffer += message
