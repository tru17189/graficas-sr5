import struct
from random import randint as random 

def char(c):
    return struct.pack("=c", c.encode("ascii"))

def word(c):
    return struct.pack("=h", c)

def dword(c):
    return struct.pack("=l", c)

def color (r, g, b):
    return bytes([b, g, r])

def glInit():
    r.__init__()

def glCreateWindow(width, height):
   r.CreateW(width, height)

def glFinish(filename):
    r.write(filename)

def point(x, y, color):
    r.point(x, y, color)

def line(x1,y1,x2,y2, color):
    dy = abs(y2-y1)
    dx = abs(x2-x1)

    steep = dy > dx

    if steep:
        x1, y1 = y1 ,x1
        x2,y2=y2,x2

        dy=abs(y2-y1)
        dx=abs(x2-x1)

    if x1>x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    offset = 0 * 2 * dx
    threshold = 0.5 * 2 * dx

    y = y1

    for x in range(x1,x2+1):
        if steep:
            r.point(y,x, color)
        else:
            r.point(x,y, color)
        offset += dy
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += 1 * dx
            
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_color = WHITE
        self.clear()
        self.texture = None
        self.shader = None
        self.normalmap = None

    def clear(self):
        self.framebuffer = [
            [color(0, 0, 0)for x in range(self.width)]
            for y in range(self.height)
        ]

        self.pixels = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        #file header 14
        f.write(char("B"))
        f.write(char("M"))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        
        #Image header 40
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width + self.height *3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

    def point(self, x, y, color):
        self.framebuffer[y][x]=color

    def set_color(self, color):
        self.current_color = color

    def CreateW(self, width, height):
        self.width = width
        self.height = height
        self.clear()


r=Bitmap(1000,1000)
