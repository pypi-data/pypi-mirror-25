from __future__ import print_function, absolute_import, unicode_literals, division


from socketIO_client import SocketIO, LoggingNamespace


from threading import Thread
import time
from . import utils



class ControllerWSClient(object):

    def __init__(self, host = "0.0.0.0", port = 4567, decode_fn = utils.raw_base64_to_np_array):
        super(ControllerWSClient, self).__init__()

        self._port = port
        self._host = host
        self._decode_fn = decode_fn

        self._on_connect = []
        self._on_telemetry = []

        self._sio = None


    def __del__(self):
        if self._sio:
            self._sio.dis_connect()


    def start(self):
        self._sio = SocketIO(self._host, self._port, logger = True)

        self._sio.on('connect', self._connect)
        self._sio.on('telemetry', self._telemetry)


        self._thread = Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()


    def _run(self):
        self._sio.wait()


    def _telemetry(self, data):
        # print("_telemetry", sid)
        if data:

            if "image" in data:
                imgString = data["image"]
                data["image"] = self._decode_fn(imgString)

            for f in self._on_telemetry:
                f(data)

        else:
            # NOTE: DON'T EDIT THIS.
            self._sio.emit('manual', {})



    def _connect(self):
        for f in self._on_connect:
            f()


    def emit(self, **kwargs):
        self._sio.emit(
            "steer",
            { key : str(value) for key, value in kwargs.items() }
        )

    def on_message(self, f):

        self._on_telemetry.append(f)

        return f

    def on_connect(self, f):

        self._on_connect.append(f)

        return f




class CarWSClient(object):

    def __init__(self, host = "localhost", port = 4567):
        super(CarWSClient, self).__init__()

        self._port = port
        self._host = host

        self._on_connect = []
        self._on_steer = []
        self._sio = None


    def __del__(self):
        if self._sio:
            self._sio.dis_connect()


    def start(self):
        self._sio = SocketIO(self._host, self._port)

        self._sio.on('steer', self._steer)
        self._sio.on('connect', self._connect)

        self._thread = Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        self._sio.wait()


    def _steer(self, data):

        for f in self._on_steer:
            f(data)



    def _connect(self):
        for f in self._on_connect:
            f()


    def emit(self, **kwargs):
        self._sio.emit(
            "telemetry",
            { key : str(value) for key, value in kwargs.items() }
        )

    def on_message(self, f):

        self._on_steer.append(f)

        return f

    def on_connect(self, f):

        self._on_connect.append(f)

        return f
