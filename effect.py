import socket
import time
import sys
import os
import math
import time
from colorsys import *
from twisted.internet import protocol, reactor, endpoints
from twisted.internet.protocol import DatagramProtocol
from threading import Thread

'''
    This code is ugly and I know it.
    - Konrad Beckmann
'''

UDP_PORT = 10001
BULB_TIME_TO_LIVE = 20
ANIMATION_SPEED = 30.0 # in FPS
TIME_PER_FRAME = 1/ANIMATION_SPEED

PIXELS = 64
BPP = 3
BRIGHTNESS = 128.0

SIN_CHANGE_PER_TIME = 0.5
SIN_CHANGE_PER_PX   = 3.0
SIN_SIZE_PER_STRIP  = 20.0

bulbs = dict()

def render(buf, i):
    for x in range(0, PIXELS/2):
        hue = math.sin((i*SIN_CHANGE_PER_TIME + x*SIN_CHANGE_PER_PX) / SIN_SIZE_PER_STRIP)
        normalized_hue = (hue + 1.0) / 2 # Normalized to 0..1
        r,g,b = hsv_to_rgb(normalized_hue, 1.0, 1.0)
        r = int(r * BRIGHTNESS)
        g = int(g * BRIGHTNESS)
        b = int(b * BRIGHTNESS)

        buf[x*BPP + 0] = g
        buf[x*BPP + 1] = r
        buf[x*BPP + 2] = b

        x2 = PIXELS - x - 1
        buf[x2*BPP + 0] = g
        buf[x2*BPP + 1] = r
        buf[x2*BPP + 2] = b


def animate():
    timestamp = 0

    # Set broadcast mode
#    if hasattr(socket,'SO_BROADCAST'):
#        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        new_time = time.time()
        time_to_wait = min(TIME_PER_FRAME, abs(timestamp + TIME_PER_FRAME - new_time))
        process_all_bulbs()
        time.sleep(time_to_wait)
        timestamp = new_time


def process_a_bulb(ip, timestamp, counter):
#    print "Process bulb %s \t- %s \t- %s" % (str(ip), str(timestamp), str(counter))
    data = bytearray(PIXELS * BPP)
    render(data, counter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(data[0:PIXELS * BPP]), (ip, UDP_PORT))
    counter += 1
    bulbs[ip] = (timestamp, counter)


def process_all_bulbs():
    for ip in bulbs.keys():
        timestamp, counter = bulbs[ip]
        if (time.time() - timestamp < BULB_TIME_TO_LIVE):
#            print "Animating bulb %s" % str(ip)
            process_a_bulb(ip, timestamp, counter)
        else:
            print "Removing stale bulb %s" % str(ip)
            del bulbs[ip]
        


def heartbeat(ip):
    timestamp = time.time()
    if ip in bulbs:
        _, counter = bulbs[ip]
        bulbs[ip] = (timestamp, counter)
    else:
        bulbs[ip] = (timestamp, 0)
        print "New bulb found - %s for a total of\t%d" % (str(ip), len(bulbs))


class HeartbeatReciever(DatagramProtocol):
    def __init__(self):
        pass

    def startProtocol(self):
        "Called when transport is connected"
        pass

    def stopProtocol(self):
        "Called after all transport is teared down"


    def datagramReceived(self, data, (ip, port)):
        if (str(data) == ip):
          heartbeat(ip)


if __name__ == "__main__":
    try:
        print("Starting up..")
        reactor.listenMulticast(10000, HeartbeatReciever(), listenMultiple=True)
        Thread(target=reactor.run, args=(False,)).start()

        while True:
            animate()

    except KeyboardInterrupt:
        os._exit(1)
        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
