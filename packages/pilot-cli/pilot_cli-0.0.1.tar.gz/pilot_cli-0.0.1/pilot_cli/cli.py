from .extra_environments import ViewerEnv, KeyboardControllerEnv, KeyboardControllerViewerEnv
import click
import time



@click.group()
def main():
    pass


@main.command()
@click.option('--host', '-h', default = "0.0.0.0")
@click.option('--port', '-p', default = 4567)
@click.option('--mode', '-m', default = "client")
@click.option('--dont-wait', is_flag = True)
@click.option('--renderer', '-r', default = "plt")
@click.option('--show-fps', is_flag = True)
@click.option('--timeout', '-t', default = 0.01)
@click.option('--dont-render', is_flag = True)
def viewer(host, port, mode, dont_wait, renderer, show_fps, timeout, dont_render):
    # port = int(port)
    wait_next = not dont_wait

    c = ViewerEnv(host = host, mode = mode, port = port, wait_next = wait_next, renderer = renderer)

    while True:
        t0 = time.time()

        if not dont_render:
            c.render()
        else:
            c.get_data()

        fps = 1.0 / (time.time() - t0)

        if show_fps:
            print("FPS: {}".format(fps))

        if not wait_next:
            time.sleep(timeout)


@main.command()
@click.option('--host', '-h', default = "0.0.0.0")
@click.option('--port', '-p', default = 4567)
@click.option('--mode', '-m', default = "client")
@click.option('--dont-wait', is_flag = True)
@click.option('--lib', '-l', default = "pynput")
@click.option('--steering-angle', default = 0.5)
@click.option('--throttle', default = 0.5)
def controller(host, port, mode, dont_wait, lib, steering_angle, throttle):
    # port = int(port)
    wait_next = not dont_wait

    c = KeyboardControllerEnv(emit_on_callback = True, host = host, mode = mode, port = port, wait_next = wait_next, lib = lib, steering_angle = steering_angle, throttle = throttle)

    while True:
        # c.step()
        time.sleep(1)



@main.command("viewer-controller")
@click.option('--host', '-h', default = "0.0.0.0")
@click.option('--port', '-p', default = 4567)
@click.option('--mode', '-m', default = "client")
@click.option('--dont-wait', is_flag = True)
@click.option('--renderer', '-r', default = "plt")
@click.option('--show-fps', is_flag = True)
@click.option('--timeout', '-t', default = 0.01)
@click.option('--dont-render', is_flag = True)
@click.option('--lib', '-l', default = "pynput")
@click.option('--steering-angle', default = 0.5)
@click.option('--throttle', default = 0.5)
def viewer_controller(host, port, mode, dont_wait, renderer, show_fps, timeout, dont_render, lib, steering_angle, throttle):
    # port = int(port)
    wait_next = not dont_wait

    c = KeyboardControllerViewerEnv(emit_on_callback = True, host = host, mode = mode, port = port, wait_next = wait_next, renderer = renderer, lib = lib, steering_angle = steering_angle, throttle = throttle)

    while True:
        t0 = time.time()

        if not dont_render:
            c.render()
        else:
            c.get_data()

        fps = 1.0 / (time.time() - t0)

        if show_fps:
            print("FPS: {}".format(fps))

        if not wait_next:
            time.sleep(timeout)
