from __future__ import print_function, absolute_import, unicode_literals, division

from . import clients
from . import servers

import time
from abc import ABCMeta, abstractproperty, abstractmethod


class BaseEnv(object):

    __metaclass__ = ABCMeta

    """docstring for BaseEnv."""
    def __init__(self, *args, **kwargs):
        super(BaseEnv, self).__init__()

        mode = kwargs.pop("mode", "client")
        self._wait_next = kwargs.pop("wait_next", False)
        self._emit_on_callback = kwargs.pop("emit_on_callback", False)

        self._command = kwargs.pop("initial_command", self.initial_command)
        self._data = kwargs.pop("initial_data", self.initial_data)
        self._socket_obj = kwargs.pop("socket_obj", None)

        start = True

        if self._socket_obj is not None:
            start = False
        elif mode == "client":
            self._socket_obj = self.client_class(*args, **kwargs)
        elif mode == "server":
            self._socket_obj = self.server_class(*args, **kwargs)
        else:
            raise Exception("Mode '{}' not supported".format(mode))

        print(self._socket_obj)
        self._socket_obj.on_message(self.on_message)

        if start:
            print("before start")
            self._socket_obj.start()
            print("after start")

        if self._emit_on_callback:
            self._socket_obj.emit(**self._command)


    @abstractproperty
    def initial_command(self):
        pass

    @abstractproperty
    def initial_data(self):
        pass

    @abstractproperty
    def server_class(self):
        pass

    @abstractproperty
    def client_class(self):
        pass

    def on_message(self, data):
        self._data = data

        if self._emit_on_callback:
            self._socket_obj.emit(**self._command)


    def get_data(self, wait_next = None):
        wait_next = wait_next if isinstance(wait_next, (bool, int, float)) else self._wait_next

        if wait_next:
            if isinstance(wait_next, bool):
                self._data = None
                while self._data is None:
                    time.sleep(0.001)
            else:
                time.sleep(wait_next)

        return self._data

    def set_command(self, **kwargs):
        self._command = kwargs

    def emit(self, **kwargs):
        if kwargs:
            self._command = kwargs

        # print(self._socket_obj)
        self._socket_obj.emit(**self._command)


    def step(self, **kwargs):
        self.set_command(**kwargs)

        if not self._emit_on_callback:
            self.emit()

        return self.get_data()


    def reset(self):
        return self.get_data(wait_next = True)


class CarEnv(BaseEnv):
    """docstring for CarEnv."""

    @property
    def initial_command(self):
        return dict()

    @property
    def initial_data(self):
        return dict()

    @property
    def server_class(self):
        return servers.CarWSServer

    @property
    def client_class(self):
        return clients.CarWSClient



class ControllerEnv(BaseEnv):
    """docstring for ControllerEnv."""

    @property
    def initial_command(self):
        return dict(
            steering_angle = 0.0,
            throttle = 0.0
        )

    @property
    def initial_data(self):
        return dict()

    @property
    def server_class(self):
        return servers.ControllerWSServer

    @property
    def client_class(self):
        return clients.ControllerWSClient
