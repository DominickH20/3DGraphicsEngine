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


class axes(WorldObjects):
    def __init__(self, size):
        WorldObjects.__init__(self,[[size,0,0],[0,size,0],[0,0,size],[0,0,0]]) #Offset from origin for projection

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
