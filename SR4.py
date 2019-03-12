import SR2_1
import OBJ
from OBJ import obj, Texture
from collections import namedtuple
def color (r, g, b):
    return bytes([b, g, r])

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
zbuffer=[]
pixels=[]

def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1): 
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,)

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  v0 = V3(*v0)
  v0length = length(v0)
  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()

  return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

def barycentric(A, B, C, P):
    bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary[2]) < 1:
        return -1, -1, -1   

    return (
        1 - (bary[0] + bary[1]) / bary[2],
        bary[1] / bary[2],
        bary[0] / bary[2]
        )

def ndc(point):
  point = V3(*point)
  return V3(
    point.x / point.z,
    point.y / point.z,
    point.z / point.z
  )


BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

def transform(vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    
    return V3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2])
    )
    return(V2(xs[0], ys[0]), V2(xs[2], ys[2]))

def display(filename='imagen.bmp'):
    SR2_1.glFinish(filename)
    try:
      from wand.image import Image
      from wand.display import display

      with Image(filename=filename) as image:
        display(image)
    except ImportError:
      pass

def boundingBox(A, B, C):
    a = [A.x, B.x, C.x]
    a.sort()

    b = [A.y, B.y, C.y]
    b.sort()
    xs = a
    ys = b

    return(V2(xs[0], ys[0]), V2(xs[2], ys[2]))


def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()
    self.texture = None
    self.shader = None
    self.normalmap = None

def clear():
    global zbuffer
    global pixels
    height = 1000
    width = 1000
    pixels = [
      [WHITE for x in range(width)] 
      for y in range(height)
    ]
    zbuffer = [
      [-float('inf') for x in range(width)]
      for y in range(height)
    ]

clear()
def triangle2(A, B, C, color=None, texture_coords=(), varying_normals=()):
    texture = None
    shader = None
    normalmap = None
    bbox_min, bbox_max = boundingBox(A, B, C)
    #print(A,B,C)
    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V2(x, y))
        if w < 0 or v < 0 or u < 0:  
          continue

        z = A.z * w + B.z * v + C.z * u

        if x < len(zbuffer) and y < len(zbuffer[x]) and z >zbuffer[x][y]:
            SR2_1.point(x, y, color)
            zbuffer[x][y] = z

def load(filename, filename2, a, b, c, translate = (0, 0, 0), scale = (1, 1, 1)):
    model = OBJ.obj(filename, filename2)
    k = a
    l= b
    z = c

    light = V3(0, 0, 1)

    for face in model.faces:
        vcount = len(face)

        if vcount == 3:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            a=V3(*model.vertices[f1])
            b=V3(*model.vertices[f2])
            c=V3(*model.vertices[f3])


            normal = norm(cross(sub(b, a), sub(c, a)))
            intensity = dot(normal, light)
            gray = round(k  * intensity)
           
            a = transform(a, translate, scale)
            b = transform(b, translate, scale)
            c = transform(c, translate, scale)
            
            if intensity < 0:
                continue

            triangle2(a,b,c,color(gray, gray, gray))

load("Cartman1.obj","Cartman1.mtl", 10, 10, 255, (-1,-1.5,1), (800,800,200))
SR2_1.glFinish("x.bmp")
