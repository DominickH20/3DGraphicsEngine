import math

#representation of a vector in R3
class vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y

    def setZ(self,z):
        self.z = z

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"


#set of operations in R3 that are useful for the purposes of this project
def dot(a,b):
    return a.x*b.x + a.y*b.y + a.z*b.z

def cross(a,b):
    return vector(a.y*b.z-a.z*b.y,-(a.x*b.z-a.z*b.x),a.x*b.y-a.y*b.x)

def add(a,b):
    return vector(a.x+b.x,a.y+b.y,a.z+b.z)

def scalarMult(a,k):
    return vector(k*a.x,k*a.y,k*a.z)

def subtract(a,b):
    return add(a,scalarMult(b,-1))

def normalize(a):
    return vector(a.x/a.mag(),a.y/a.mag(),a.z/a.mag())
