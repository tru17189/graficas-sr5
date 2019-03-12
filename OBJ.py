class obj(object):
    def __init__(self, filename, filename2):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        with open(filename2) as ff:
            self.lines1 = ff.read().splitlines()
        self.vertices = []
        self.faces = []
        self.usemtl = []
        self.kd = []
        self.material = ""
        self.materials = {}
        self.read()

    def try_int(self, something):
        try:
            int(something)
        except ValueError:
            print()

    def mtl(self, e):
        for linee in self.lines1:
            if linee:
                if linee.find(e)!=-1:
                    self.material = e
                if linee.find("Kd")!=-1:
                    prefix, value = linee.split(' ', 1)
                    if prefix == 'Kd':
                        kd = []
                        kd = list(map(float, value.split(' ')))
                        self.materials[self.material] = kd
                        
            

    def read(self):
        self.mate = ""
        for line in self.lines:
            if line:
                if line.find("//")!=-1:
                    line=line.replace("//", "/0/")
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int, face.split('/'))) for face in value.split(' ')])
                if line.find("usemtl")!=-1:
                    self.usemtl=value #.append(list(map(str,value.split(' '))))
                    e = str(self.usemtl)
                    if e != "None":
                        self.mate = e
                        self.mtl(e)
                    

                
class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        
        image.seek(2 + 4 + 4)  
        header_size = struct.unpack("=l", image.read(4))[0]  
        image.seek(2 + 4 + 4 + 4 + 4)
        
        self.width = struct.unpack("=l", image.read(4))[0]  
        self.height = struct.unpack("=l", image.read(4))[0]  
        self.pixels = []
        image.seek(header_size)
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r,g,b))
        image.close()

    def get_color(self, tx, ty):
        x = int(tx * self.width)
        y = int(ty * self.height)
        return self.pixels[y][x]

