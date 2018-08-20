import weakref
from math import *

class WorldObjects:
    instances = set()
    def __init__(self, vertices):
        self.vertices = vertices
        WorldObjects.instances.add(weakref.ref(self))

    @classmethod            ####OBJECT TRACKING TAKEN FROM http://effbot.org/pyfaq/how-do-i-get-a-list-of-all-instances-of-a-given-class.htm
    def getinstances(cls):
        dead = set()
        for ref in cls.instances:
            obj = ref()
            if(obj is not None):
                yield obj
            else:
                dead.add(ref)
        cls.instances -= dead

    globalMesh = []

class axes(WorldObjects):
    def __init__(self, size):
        WorldObjects.__init__(self,[[size,0,0],[0,size,0],[0,0,size],[0,0,0]]) #Offset from origin for projection

class flatPlane(WorldObjects):
    def __init__(self, size, z, color):
        self.color = color
        WorldObjects.__init__(self, [[size,size,z],[-size,size,z],[-size,-size,z],[size,-size,z]])
        self.globalMesh.append([[[size,size,z],[-size,size,z],[-size,-size,z],[size,-size,z]], color])

class cube(WorldObjects):
    def __init__(self,size, c1, c2, c3, color):
        self.color = color
        a1 = c1+int(size/2)
        a2 = c2 + int(size / 2)
        a3 = c3 + int(size / 2)
        WorldObjects.__init__(self, [[a1,a2,a3],[a1,a2-size,a3],[a1,a2-size,a3-size],[a1,a2,a3-size],[a1-size,a2,a3],[a1-size,a2-size,a3],[a1-size,a2-size,a3-size],[a1-size,a2,a3-size]])
        #build meshes by listing vertices ccw (from exterior)
        self.globalMesh.append([[[a1,a2,a3],[a1,a2-size,a3],[a1,a2-size,a3-size],[a1,a2,a3-size]], color])
        self.globalMesh.append([[[a1,a2,a3],[a1,a2,a3-size],[a1-size,a2,a3-size],[a1-size,a2,a3]],color])
        self.globalMesh.append([[[a1-size,a2,a3],[a1-size,a2,a3-size],[a1-size,a2-size,a3-size],[a1-size,a2-size,a3]],color])
        self.globalMesh.append([[[a1-size,a2-size,a3],[a1-size,a2-size,a3-size],[a1,a2-size,a3-size],[a1,a2-size,a3]],color])
        self.globalMesh.append([[[a1,a2,a3],[a1-size,a2,a3],[a1-size,a2-size,a3],[a1,a2-size,a3]],color])
        self.globalMesh.append([[[a1,a2,a3-size],[a1,a2-size,a3-size],[a1-size,a2-size,a3-size],[a1-size,a2,a3-size]],color])

class surface(WorldObjects):
    def __init__(self,size, increment, color):
        self.color = color
        for x in range(-size-increment,size,increment):
            for y in range(-size-increment,size,increment):
                self.globalMesh.append([[[x,y,(x^2+y^2)/30],[x-increment,y,((x-increment)^2+y^2)/30],[x-increment,y-increment,((x-increment)^2+(y-increment)^2)/30],[x,y-increment,(x^2+(y-increment)^2)/30]],color])

        """
        vertices = [[[] for i in range(-size,size)] for i in range(-size,size)]
        #print(vertices)
        vertices[0][0]=[1]
        masterlist = []
        for x in range(-size,size):
            for y in range(-size,size):
                vertices[x][y]=[sin(x*y/300)]
                masterlist.append([x,y,vertices[x][y][0]])
        WorldObjects.__init__(self, masterlist)
        print(masterlist)
        #self.globalMesh.append([[[0,0,vertices[0][0][0]],[0,1,vertices[0][1][0]],[1,0,vertices[1][0][0]]],color])
        #self.globalMesh.append([[[0,0,0],[0,300,300],[-20,20,40]],color])
        for x in range(-size+1,size-1):
            for y in range(-size+1,size-1):
                self.globalMesh.append([[[x,y,vertices[x][y][0]],[x-1,y,vertices[x-1][y][0]],[x-1,y-1,vertices[x-1][y-1][0]],[x,y-1,vertices[x][y-1][0]]],color])
        """



class lattice(WorldObjects):
    def __init__(self, size, zlevel):
        WorldObjects.__init__(self,[[size, size, zlevel],[-size, size, zlevel],[-size, -size, zlevel],[size, -size, zlevel]])

class wireCube(WorldObjects):
    def __init__(self, c1, c2, c3, size, color):
        self.color = color
        a1 = c1 - size
        a2 = c2 - size
        a3 = c3 - size
        leng = 2*size
        vertices = [[a1,a2,a3],[a1+leng,a2,a3],[a1,a2+leng,a3],[a1+leng,a2+leng,a3],[a1,a2,a3+leng],[a1+leng,a2,a3+leng],[a1,a2+leng,a3+leng],[a1+leng,a2+leng,a3+leng]]
        WorldObjects.__init__(self,vertices)

class helix(WorldObjects):
    def __init__(self, radius, start, end, incline, increment, speed, color):
        self.color = color
        self.radius = radius
        self.start = start
        self.end = end
        self.incline = incline
        self.increment = increment
        self.speed = speed
        WorldObjects.__init__(self,self.genVertices(self.radius,self.start,self.end,self.incline,self.increment, self.speed))

    def genVertices(self, radius, start, end, incline, increment, speed):
        vertices = []
        for t in range(start,end,increment):
            vertices.append([radius*cos(t/speed),radius*sin(t/speed),t])
        return vertices

    def updateVertices(self, radius, start, end, incline, increment, speed,color):
        self.color = color
        vertices = []
        for t in range(start,end,increment):
            vertices.append([radius*cos(t/speed),radius*sin(t/speed),t])
        self.vertices = vertices
