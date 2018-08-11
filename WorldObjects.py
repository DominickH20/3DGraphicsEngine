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

