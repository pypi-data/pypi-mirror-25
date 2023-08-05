from __future__ import print_function, absolute_import, unicode_literals, division


import socketio
from flask import Flask
from eventlet import wsgi, listen
import eventlet
from threading import Thread
import time
from . import utils
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


class WSServer(object):

    def __init__(self, host = '', port = 4567, decode_fn = utils.raw_base64_to_np_array, logger = False, async_mode = "eventlet", ignore_queue = False):
        super(WSServer, self).__init__()

        self._sio = socketio.Server(logger=logger, async_mode = "eventlet")

        self._host = host
        self._port = port
        self._decode_fn = decode_fn
        self._async_mode = async_mode
        self._ignore_queue = ignore_queue

        self._sio.on("steer")(self._steer)
        self._sio.on("telemetry")(self._telemetry)
        # self._sio.on("connect")(lambda sid, *args: self._sio.emit("connect"))

        self._app = Flask(__name__)

        if self._async_mode == "eventlet" or self._async_mode == "threading":
            self._app = socketio.Middleware(self._sio, self._app)

        elif self._async_mode == "gevent":
            self._app.wsgi_app = socketio.Middleware(self._sio, self._app.wsgi_app)
        else:
            raise Exception("async_mode '{}' invalid".format(async_mode))


    def start(self):
        self._thread = Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()


    def _steer(self, sid, data):
        return self._sio.emit("steer", data = data, ignore_queue = self._ignore_queue)

    def _telemetry(self, sid, data):
        # print(data)
        return self._sio.emit("telemetry", data = data, ignore_queue = self._ignore_queue)

    def _run(self):
        if self._async_mode == "eventlet" or self._async_mode == "threading":
            eventlet.wsgi.server(eventlet.listen((self._host, self._port)), self._app)
        elif self._async_mode == "gevent":
            pywsgi.WSGIServer((self._host, self._port), self._app).serve_forever()
        # self._app.run(threaded=True, host = self._host, port = self._port)


    def __del__(self):
        self._sio.dis_connect()



class ControllerWSServer(WSServer):
    """docstring for ControllerWSServer."""
    def __init__(self, *args, **kwargs):
        self._on_telemetry = []

        super(ControllerWSServer, self).__init__(*args, **kwargs)

    def _telemetry(self, sid, data):
        super(ControllerWSServer, self)._telemetry(sid, data)

        if data:

            if "image" in data:
                imgString = data["image"]
                data["image"] = self._decode_fn(imgString)

            for f in self._on_telemetry:
                f(data)

        else:
            # NOTE: DON'T EDIT THIS.
            self._sio.emit('manual', {})

    def on_message(self, f):

        self._on_telemetry.append(f)

        return f

    def emit(self, **kwargs):
        self._sio.emit(
            "steer",
            data = { key : str(value) for key, value in kwargs.items() }
        )

class CarWSServer(WSServer):
    """docstring for CarWSServer."""
    def __init__(self, *args, **kwargs):
        self._on_steer = []


        super(CarWSServer, self).__init__(*args, **kwargs)


    def _steer(self, sid, data):
        super(ControllerWSServer, self)._steer(sid, data)

        for f in self._on_steer:
            f(data)

    def on_message(self, f):

        self._on_steer.append(f)

        return f

    def emit(self, **kwargs):
        # print(kwargs)
        self._sio.emit("telemetry", data = { key : str(value) for key, value in kwargs.items() })
