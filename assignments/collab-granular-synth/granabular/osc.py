import time
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

def send_slider_value(id, value):
    # Build a message with autodetection of data types, and send it.
    msg = oscbuildparse.OSCMessage(f"/sliders/{id}", ",i", [value])
    osc_send(msg, "Pd")
    osc_process()

def send_grain_file(value):
    # Build a message with autodetection of data types, and send it.
    msg = oscbuildparse.OSCMessage(f"/grains", ",i", [value])
    osc_send(msg, "Pd")
    osc_process()