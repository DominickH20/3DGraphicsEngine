import weakref
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
        WorldObjects.__init__(self,[[size,0,0],[0,size,0],[0,0,size],[0,0,0]])

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