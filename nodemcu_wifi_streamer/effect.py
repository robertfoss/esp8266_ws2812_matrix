import socket
import time
import math
from colorsys import *

'''
    This code is ugly and I know it.
    - Konrad Beckmann
'''

W = 144
H = 8
BPP = 3

class Foo():
    def __init__(self):
        self.i = 0

    def clamp(self, x, a, b):
        return max(min(x, b), a)

    def setpixel(self, buf, x, y, rgb):
        oldx=x
        if y % 2 == 1: x = W - 1 - x
        try:
            buf[x*BPP + W*BPP*y]     = int(rgb[1])
            buf[x*BPP + W*BPP*y + 1] = int(rgb[0])
            buf[x*BPP + W*BPP*y + 2] = int(rgb[2])
        except:
            print oldx, y, rgb

    def lissajous(self, A, a, B, b, x0, y0, delta, t):
        x = x0 + A * math.sin(a * t + delta)
        y = y0 + B * math.sin(b * t)
        return (x, y)

    def render_lissajous(self, buf, u, v, A, a, B, b, x0, y0, delta, t, intensity):
        (x, y) = self.lissajous(A + v, a, B + v, b, u, 4, self.i / 10.0, self.i / 10.0 + t/100.0)
        (r, g, b) = hsv_to_rgb(t / 100.0, 1.0, 1.0)
        r = int(r*16 * intensity)
        g = int(g*16 * intensity)
        b = int(b*16 * intensity)
        if y >= 0 and y < H:
            self.setpixel(buf, self.clamp(int(x + 70), 0, W - 1), self.clamp(int(y), 0, 7), (r, g, b))

    def render_curves(self, buf):
        i = self.i
        u1 = 40 * math.sin(i / 10.0 + math.pi)    
        u2 = 40 * math.sin(i / 10.0)    
        v1 = 2.5 * math.sin(i / 10.0 + 3 * math.pi / 2)
        v2 = 2.5 * math.sin(i / 10.0 + math.pi / 2)
        i1 = v1 / 6 + 1
        i2 = v2 / 6 + 1
        
        if v1 < 0:
            for t in range(0, 300):
                self.render_lissajous(buf, u1, v1,  20, 6, 4, 6, u1, 4, 0, t, i1)
            for t in range(0, 300):
                self.render_lissajous(buf, u2, v2,  20, 3, 4, 6, u2, 4, 0, t, i2)
        else:
            for t in range(0, 300):
                self.render_lissajous(buf, u2, v2,  20, 3, 4, 6, u2, 4, 0, t, i2)
            for t in range(0, 300):
                self.render_lissajous(buf, u1, v1,  20, 6, 4, 6, u1, 4, 0, t, i1)

    def render_background(self, buf):
        for y in range(0, H):
            for x in range(0, W):
                self.setpixel(buf, x, y, self.funky(x, y))
        
    def funky(self, x, y):
        x = (x + int(30 * math.sin((self.i+y) / 3.0))) % W
        h = math.fmod((x + 30 * (1.0 + math.sin(self.i / 5.0))) / W, 1.0)
        rgb = hsv_to_rgb(h, 1.0, 1.0)
        v = (math.sin(self.i / 3.0) + 1.0) + 1.5
        r = rgb[0] * 2.0 * v * 8
        g = rgb[1] * 2.0 * v * 8
        b = rgb[2] * 2.0 * v * 8

        return (int(r), int(g), int(b))
    
    def main(self):
        UDP_IP = "192.168.1.38"
        UDP_PORT = 8888
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        while True:
            self.i = (self.i + 1)
            data = bytearray(W * H * BPP)
        
            self.render_background(data)
            #self.render_curves(data)

            sock.sendto(bytes(data[0:500]), (UDP_IP, UDP_PORT))
            time.sleep(0.02)

if __name__ == "__main__":
    while True:
        try:
            Foo().main()
        except KeyboardInterrupt:
            break
        except:
            pass
