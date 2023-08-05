import sys, os
sys.path.append("pilot_cli")


###### controller
from servers import WSServer
server = WSServer()
server.start()




from servers import WSServer
from clients import CarWSClient, ControllerWSClient



server = WSServer()

car = CarWSClient()
controller = ControllerWSClient()

@car.on_connect
def connected():
    print("car connected")


@controller.on_telemetry
def tel(data):
    print("TELEMETRY")
    print(data)

server.start()

car.start()
car._sio.connect()
controller.start()
controller._sio.connect()

@car.on_steer
def on_steer(data):
    print("STEER", data)

controller.steer(
    steering_angle = 0.1,
    throttle = 0.2
)

controller._sio.emit("steer", "1,2,3")
car.telemetry(a = 1)
