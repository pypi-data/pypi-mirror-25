from __future__ import print_function, absolute_import, unicode_literals, division

import base64
import numpy as np
import socketio
from PIL import Image
from io import BytesIO
from flask import Flask
import eventlet
from threading import Thread
import time
# from base import BaseEnv


class UdacityEnv(object):

    def __init__(self):
        super(UdacityEnv, self).__init__()

        self._sio = socketio.Server()

        self._sio.on('telemetry')(self._telemetry)
        self._sio.on('connect')(self._connect)

        self._app = Flask(__name__)
        self._app = socketio.Middleware(self._sio, self._app)

        self._steering_angle = 0.0
        self._throttle = 0.0
        self._speed = 0.0
        self._image = None

        self._thread = Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()




    def reset(self):
        while self._image is None:
            time.sleep(0.01)

        return dict(
            image = self._image,
            speed = self._speed
        )



    def step(self, action):
        if type(action) is dict:
            self._set_control(action["steering_angle"], action["throttle"])
        else:
            self._set_control(action[0], action[1])

        return dict(
            image = self._image,
            speed = self._speed
        )



    def _run(self):
        eventlet.wsgi.server(eventlet.listen(('', 4567)), self._app)


    def _telemetry(self, sid, data):
        # print("_telemetry", sid)
        if data:
            # The current steering angle of the car
            steering_angle = data["steering_angle"]
            # The current throttle of the car
            throttle = data["throttle"]
            # The current speed of the car
            self._speed = data["speed"]
            # The current image from the center camera of the car
            imgString = data["image"]
            image = Image.open(BytesIO(base64.b64decode(imgString)))

            #update
            self._image = np.asarray(image)

            self._send_control()
        else:
            # NOTE: DON'T EDIT THIS.
            self._sio.emit('manual', data={})

        # print("tel-done")



    def _connect(self, sid, environ):
        pass
        # print("_connect ", sid, environ)


    def _send_control(self):
        self._sio.emit(
            "steer",
            data = {
                'steering_angle': str(self._steering_angle),
                'throttle': str(self._throttle)
            }
        )
        # print("sent")

    def __del__(self):
        self._sio.dis_connect()


    def _set_control(self, steering_angle, throttle):
        self._steering_angle = steering_angle
        self._throttle = throttle


# env = UdacityEnv()
# x = env.reset()
# x

if __name__ == '__main__':
    pass
