

from .environments import ControllerEnv
import base64
import numpy as np
import keyboard
import threading
import time
import pynput


class ListenerEnv(ControllerEnv):
    """docstring for ViewerEnv."""

    def __init__(self, *args, **kwargs):

        self._callback = kwargs.pop("on_message")

        super(ListenerEnv, self).__init__(*args, **kwargs)



    def on_message(self, data):
        super(ListenerEnv, self).on_message(data)

        self._callback(data)




class ViewerEnv(ControllerEnv):
    """docstring for ViewerEnv."""

    def __init__(self, *args, **kwargs):

        self._renderer = kwargs.pop("renderer", "plt")

        renderers = ["plt", "cv2"]
        if self._renderer not in renderers:
            raise Exception("Renderer '{}' not supported. Use {}".format(self._renderer, renderers))

        if self._renderer == "cv2":
            def decode_fn(s):
                try:
                    s = base64.decodestring(s)
                    np_arr = np.fromstring(s, np.uint8)
                    img = self._cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    return img
                except Exception as e:
                    print(e)
                    return str(e)

            kwargs["decode_fn"] = decode_fn


        if self._renderer == "plt":
            from matplotlib import pyplot as plt
            self._plt = plt

            self._f = plt.figure()
            self._ax = self._f.gca()
            self._f.show()

        else:
            import cv2
            self._cv2 = cv2

        super(ViewerEnv, self).__init__(*args, **kwargs)





    def render(self):
        # self.emit()
        data = self.get_data()
        if data:

            if "image" in data:
                img = data["image"]

                if self._renderer == "plt":

                    self._ax.imshow(img)
                    self._f.canvas.draw()
                else:
                    self._cv2.imshow("image", img)
                    self._cv2.waitKey(1)

            else:
                print("No image")


class KeyboardControllerEnv(ControllerEnv):

    def __init__(self, *args, **kwargs):
        self._lib = kwargs.pop("lib", "pynput")
        self._throttle = kwargs.pop("throttle", 0.5)
        self._steering_angle = kwargs.pop("steering_angle", 0.5)

        if self._lib not in ["pynput", "keyboard"]:
            raise Exception("Invalid lib {}".format(self._lib))

        super(KeyboardControllerEnv, self).__init__(*args, **kwargs)

        if self._lib == "keyboard":

            keyboard.hook_key('up', keydown_callback=lambda: self.pressed("up"), keyup_callback=lambda: self.unpressed("up"))
            keyboard.hook_key('down', keydown_callback=lambda: self.pressed("down"), keyup_callback=lambda: self.unpressed("down"))
            keyboard.hook_key('left', keydown_callback=lambda: self.pressed("left"), keyup_callback=lambda: self.unpressed("left"))
            keyboard.hook_key('right', keydown_callback=lambda: self.pressed("right"), keyup_callback=lambda: self.unpressed("right"))

            target_fn = keyboard.wait


        else:
            import pynput

            def target_fn():
                with pynput.keyboard.Listener(on_press = self.on_press, on_release = self.on_release):
                    while True:
                        time.sleep(1.0)

        t = threading.Thread(target=target_fn)
        t.daemon = True
        t.start()

    def pressed(self, key):

        if key == "up":
            self._command["throttle"] = self._throttle
        elif key == "down":
            self._command["throttle"] = -self._throttle
        elif key == "left":
            self._command["steering_angle"] = -self._steering_angle
        elif key == "right":
            self._command["steering_angle"] = self._steering_angle


    def unpressed(self, key):

        if key == "up":
            self._command["throttle"] = 0
        elif key == "down":
            self._command["throttle"] *= 0
        elif key == "left":
            self._command["steering_angle"] = 0
        elif key == "right":
            self._command["steering_angle"] = 0


    def on_press(self, key):

        if key == pynput.keyboard.Key.up:
            self.pressed("up")
        elif key == pynput.keyboard.Key.down:
            self.pressed("down")
        elif key == pynput.keyboard.Key.left:
            self.pressed("left")
        elif key == pynput.keyboard.Key.right:
            self.pressed("right")

    def on_release(self, key):

        if key == pynput.keyboard.Key.up:
            self.unpressed("up")
        elif key == pynput.keyboard.Key.down:
            self.unpressed("down")
        elif key == pynput.keyboard.Key.left:
            self.unpressed("left")
        elif key == pynput.keyboard.Key.right:
            self.unpressed("right")


class KeyboardControllerViewerEnv(ViewerEnv):

    def __init__(self, *args, **kwargs):
        self._lib = kwargs.pop("lib", "pynput")
        self._throttle = kwargs.pop("throttle", 0.5)
        self._steering_angle = kwargs.pop("steering_angle", 0.5)

        if self._lib not in ["pynput", "keyboard"]:
            raise Exception("Invalid lib {}".format(self._lib))

        super(KeyboardControllerViewerEnv, self).__init__(*args, **kwargs)

        if self._lib == "keyboard":

            keyboard.hook_key('up', keydown_callback=lambda: self.pressed("up"), keyup_callback=lambda: self.unpressed("up"))
            keyboard.hook_key('down', keydown_callback=lambda: self.pressed("down"), keyup_callback=lambda: self.unpressed("down"))
            keyboard.hook_key('left', keydown_callback=lambda: self.pressed("left"), keyup_callback=lambda: self.unpressed("left"))
            keyboard.hook_key('right', keydown_callback=lambda: self.pressed("right"), keyup_callback=lambda: self.unpressed("right"))

            target_fn = keyboard.wait
            # t = threading.Thread(target = keyboard.wait)


        else:

            listener = pynput.keyboard.Listener(on_press = self.on_press, on_release = self.on_release)
            listener.daemon = True
            listener.start()

            target_fn = lambda: listener.join()


        t = threading.Thread(target = target_fn)
        t.daemon = True
        t.start()

    def pressed(self, key):

        if key == "up":
            self._command["throttle"] = self._throttle
        elif key == "down":
            self._command["throttle"] = -self._throttle
        elif key == "left":
            self._command["steering_angle"] = -self._steering_angle
        elif key == "right":
            self._command["steering_angle"] = self._steering_angle


    def unpressed(self, key):

        if key == "up":
            self._command["throttle"] = 0
        elif key == "down":
            self._command["throttle"] *= 0
        elif key == "left":
            self._command["steering_angle"] = 0
        elif key == "right":
            self._command["steering_angle"] = 0


    def on_press(self, key):
        # print(key)
        if key == pynput.keyboard.Key.up:
            self.pressed("up")
        elif key == pynput.keyboard.Key.down:
            self.pressed("down")
        elif key == pynput.keyboard.Key.left:
            self.pressed("left")
        elif key == pynput.keyboard.Key.right:
            self.pressed("right")

    def on_release(self, key):

        if key == pynput.keyboard.Key.up:
            self.unpressed("up")
        elif key == pynput.keyboard.Key.down:
            self.unpressed("down")
        elif key == pynput.keyboard.Key.left:
            self.unpressed("left")
        elif key == pynput.keyboard.Key.right:
            self.unpressed("right")
