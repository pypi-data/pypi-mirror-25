'''
Author: Gideon Mendels

This module contains the main components of TrackML.com client side

'''
from __future__ import print_function

import inspect
import threading
import sys, os
import requests
import json
import uuid
import time
import websocket

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue


DEBUG = False

"""
A static class that handles the connection with the server.
"""


class RestServerConnection(object):
    server_address = "http://159.203.90.47/api/client-lib/"

    def __init__(self):
        pass

    @staticmethod
    def get_run_id(api_key):
        """
        Gets a new run id from the server.
        :param api_key: user's API key
        :return: run_id - String
        """
        endpoint_url = RestServerConnection.server_address + "add/run"
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        payload = {"apiKey": api_key, "local_timestamp": int(time.time() * 1000)}
        r = requests.post(url=endpoint_url, data=json.dumps(payload), headers=headers)

        if r.status_code != 200:
            raise ValueError(r.content)

        response_body = r.content

        if isinstance(response_body, bytes):
            response_body = response_body.decode("utf-8")

        run_id_server = json.loads(response_body)["runId"]
        ws_server = json.loads(response_body)["ws_url"]
        return run_id_server, ws_server

    @staticmethod
    def send_message(message):
        """
        Sends a json with stdout/metric/code to the server.
        :param message: A message object containing the values to send
        :return: True if request was sucessful.
        """
        global run_id

        if message.stdout is not None:
            base_url = RestServerConnection.server_address + "add/stdout"
        else:
            base_url = RestServerConnection.server_address + "add/data"

        headers = {'Content-Type': 'application/json;charset=utf-8'}
        r = requests.post(url=base_url, data=message.to_json(), headers=headers)

        if r.status_code != 200:
            raise ValueError(r.content + ",to address %s With request: %s" % (base_url, message))

        if run_id is None:
            run_id = json.loads(r.content)['message']

        return True


class WebSocketConnection(threading.Thread):
    def __init__(self, server_address):
        threading.Thread.__init__(self)
        self.daemon = True

        if DEBUG:
            websocket.enableTrace(True)

        self.address = server_address
        self.ws = self.connect_ws(self.address)

    def connect_ws(self, server_address):
        ws = websocket.WebSocketApp(server_address,
                                    on_message=WebSocketConnection.on_message,
                                    on_error=WebSocketConnection.on_error,
                                    on_close=WebSocketConnection.on_close)
        ws.on_open = WebSocketConnection.on_open
        return ws

    def run(self):
        self.ws.run_forever()

    def send(self, message):
        # make sure connection is actually alive
        if self.ws.sock and self.ws.sock.connected:
            payload = {}
            if message.stdout is not None:
                payload["stdout"] = message
            else:
                payload["log_data"] = message
            self.ws.send(json.dumps(payload, cls=NestedEncoder))
        else:
            self.wait_for_connection()

    def wait_for_connection(self):
        num_tries = 0
        while not self.ws.sock and not self.ws.sock.connected and num_tries < 5:
            time.sleep(1)
            num_tries += 1
            # self.ws = self.connect_ws(self.address)

        if not self.ws.sock:
            raise ValueError("Could not connect to server after multiple tries. ")

        else:
            return True

    @staticmethod
    def on_open(ws):
        if DEBUG:
            print("Socket connection open")

    @staticmethod
    def on_message(ws, message):
        if DEBUG:
            print(message)

    @staticmethod
    def on_error(ws, error):
        print(error)

    @staticmethod
    def on_close(ws):
        if DEBUG:
            print("### closed ###")


'''
This class extends threading.Thread and provides a simple concurrent queue
and an async service that pulls data from the queue and sends it to the server.
'''


class Streamer(threading.Thread):
    def __init__(self, ws_server_address):
        threading.Thread.__init__(self)
        self.daemon = True
        self.messages = queue.Queue()
        self.counter = 0
        self.websocket = WebSocketConnection(ws_server_address)
        self.websocket.start()

    def send(self, message):
        '''
        Puts a message in the queue
        :param message: Some kind of payload, type agnostic
        '''
        if message is not None:
            self.messages.put(message)

    def close(self):
        '''
        Puts a None in the queue which leads to closing it.
        '''
        self.messages.put(None)
        self.messages.join()

    def run(self):
        '''
        Continuously pulls messages from the queue and sends them to the server.
        '''
        while True:
            message = self.messages.get()
            if message is None:
                break

            # Add offset to message so server can maintain order.
            self.counter += 1
            message.set_offset(self.counter)

            try:
                # Send data to server
                # RestServerConnection.send_message(message)
                self.websocket.send(message)
                self.messages.task_done()
            except Exception as e:
                print(e, file=sys.stderr)

        self.messages.task_done()
        return


'''
A class the overwrites sys.stdout with itself.
The class prints everything as normal to console but also submits
every line to Streamer
'''


class StdLogger(object):
    # todo: this doesn't log the output from C libs (tensorflow etc)
    def __init__(self, streamer):
        '''
        :param streamer: An instance of Streamer() to allow sending to server.
        '''
        self.terminal = sys.stdout
        self.streamer = streamer
        self.api_key = None
        sys.stdout = self

    def write(self, line):
        '''
        Overrides the default IO write(). Writes to console + queue.
        :param line: String printed to stdout, probably with print()
        '''
        self.terminal.write(line)
        payload = Message(api_key=self.api_key, experiment_key=None, runId=run_id)
        payload.set_stdout(line)
        self.streamer.send(payload)

    def flush(self):
        self.terminal.flush()

    def set_api_key(self, key):
        self.api_key = key


class Message(object):
    def __init__(self, api_key, experiment_key, runId):
        self.apiKey = api_key
        self.experimentKey = experiment_key
        self.runId = runId
        self.local_timestamp = int(time.time() * 1000)

        # The following attributes are optional
        self.metric = None
        self.param = None
        self.graph = None
        self.code = None
        self.stdout = None
        self.offset = None
        self.fileName = None

    def set_offset(self, val):
        self.offset = val

    def set_metric(self, name, value):
        self.metric = {"metricName": name, "metricValue": str(value)}

    def set_param(self, name, value):
        self.param = {"paramName": name, "paramValue": str(value)}

    def set_graph(self, graph):
        self.graph = graph

    def set_code(self, code):
        self.code = code

    def set_stdout(self, line):
        self.stdout = line

    def set_filename(self, fname):
        self.fileName = fname

    def to_json(self):
        json_re = json.dumps(self.repr_json(), sort_keys=True, indent=4, cls=NestedEncoder)
        return json_re

    def repr_json(self):
        return self.__dict__

    def __str__(self):
        return self.to_json()

    def __len__(self):
        return len(self.to_json())


class NestedEncoder(json.JSONEncoder):
    '''
    A JSON Encoder that converts floats/decimals to strings and allows nested objects
    '''

    def default(self, obj):
        if isinstance(obj, float):
            return format(obj, '.2f')
        elif hasattr(obj, 'repr_json'):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)


'''
An instance of experiment. Takes the values from the different implementations and unifies them
for the server. Basically submits stuff to the Streamer queue.
'''


class Experiment(object):
    def __init__(self, api_key, log_code=True, calling_class=None):
        '''
        Init a new experiment.
        :param api_key: key used to send data to server.
        '''
        self.api_key = api_key

        # Generate a unique identifier for this experiment.
        self.id = self._generate_guid()

        global streamer
        global logger
        global run_id
        # This init the streamer and logger for the first time.
        # Would only be called once.
        if (streamer is None and logger is None):
            # Get an id for this run
            try:
                run_id, ws_server_address = RestServerConnection.get_run_id(self.api_key)
            except ValueError:
                print("Failed to establish connection to TrackML server. Please check you internet connection. Your "
                      "experiment would not be logged")

            # Initiate the streamer
            streamer = Streamer(ws_server_address)
            # Overwride default sys.stdout and feed to streamer.
            logger = StdLogger(streamer)
            # Start streamer thread.
            streamer.start()

        self.streamer = streamer
        logger.set_api_key(self.api_key)

        # This allows different implementations to provide the correct source code with logging
        # our library code.
        if log_code:
            self.set_code(self._get_source_code())

        self.set_filename(self._get_filename())

    def log_epoch_end(self, epoch_cnt):
        '''
        Logs that the current epoch finished + number. required for progress bars.
        :param epoch_cnt: integer
        '''
        message = Message(self.api_key, self.id, run_id)
        message.set_param("curr_epoch", epoch_cnt)
        self.streamer.send(message)

    def log_metric(self, name, value):
        """
        Logs a metric (i.e accuracy, f1). Required for training visualizations.
        :param name: Metric name - String
        :param value: Metric value - float
        """
        message = Message(self.api_key, self.id, run_id)
        message.set_metric(name, value)
        self.streamer.send(message)

    def log_parameter(self, name, value):
        '''
        Logs an hyper parameters
        :param name: Parameter name - String
        :param value: Parameter value - String
        '''
        message = Message(self.api_key, self.id, run_id)
        message.set_param(name, value)
        self.streamer.send(message)

    def set_code(self, code):
        '''
        Sets the current experiment script's code. Should be called once per experiment.
        :param code: String
        '''
        message = Message(self.api_key, self.id, run_id)
        message.set_code(code)
        self.streamer.send(message)

    def set_model_graph(self, graph):
        '''
        Sets the current experiment computation graph.
        :param graph: JSON
        '''
        message = Message(self.api_key, self.id, run_id)
        message.set_graph(graph)
        self.streamer.send(message)

    def set_filename(self, fname):
        message = Message(self.api_key, self.id, run_id)
        message.set_filename(fname)
        self.streamer.send(message)

    def keras_callback(self):
        from trackml.frameworks import KerasCallback
        return KerasCallback(self)

    def _get_source_code(self):
        '''
        Inspects the stack to detect calling script. Reads source code from disk and logs it.
        '''

        class_name = self.__class__.__name__

        for frame in inspect.stack():
            if frame is not None:
                if class_name in frame[4][0]:  # 4 is the position of the calling function.
                    path_to_source = frame[1]
                    if os.path.isfile(path_to_source):
                        with open(path_to_source) as f:
                            return f.read()
                    else:
                        print("failed to read source code file from disk: %s" % path_to_source, file=sys.stderr)

    def _get_filename(self):
        if len(sys.argv) > 0:
            return sys.argv[0]
        else:
            return None

    @staticmethod
    def _generate_guid():
        return str(uuid.uuid4())


streamer = None
logger = None
run_id = None
