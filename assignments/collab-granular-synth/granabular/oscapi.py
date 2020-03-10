import time
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

class osc:
    def __init__(self):
        # setup OSC comms to localhost
        osc_startup()
        osc_udp_client("127.0.0.1", 4242, "Pd")

    def send_slider_value(self, id, value):
        # Build a message with autodetection of data types, and send it.
        msg = oscbuildparse.OSCMessage(f"/sliders/{id}", ",i", [value])
        osc_send(msg, "Pd")
        osc_process()

    def send_grain_file(self, value):
        # Build a message with autodetection of data types, and send it.
        msg = oscbuildparse.OSCMessage("/grains", ",s", [value])
        osc_send(msg, "Pd")
        osc_process()
