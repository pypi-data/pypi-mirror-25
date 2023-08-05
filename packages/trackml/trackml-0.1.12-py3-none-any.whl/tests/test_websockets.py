import time
from trackml import trackml
from multiprocessing import Process
from websocket_server import WebsocketServer
import websocket_server
import json
from queue import Queue

server = None
SOCKET_PORT = 9006
last_msg = ""
our_queue = Queue()

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    global server
    import threading
    server = threading.Thread(target=websocket_server)
    server.daemon = True
    server.start()


def test_websocket(capsys):


    ws = trackml.WebSocketConnection("ws://127.0.01:" + str(SOCKET_PORT))
    ws.start()
    msg = trackml.Message("a",'b','c')
    msg.local_timestamp = None

    time.sleep(5)

    ws.send(msg)

    last_msg = our_queue.get()


    expected_json = {}
    expected_json["log_data"] = json.loads(msg.to_json())

    assert json.loads(last_msg) == expected_json



def websocket_server():
    # Called for every client connecting (after handshake)
    def new_client(client, server):
        pass

    # Called for every client disconnecting
    def client_left(client, server):
        pass

    # Called when a client sends a message
    def message_received(client, server, message):
        # echo
        our_queue.put(message)
        server.send_message_to_all(message)

    PORT = SOCKET_PORT
    server = WebsocketServer(PORT)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
