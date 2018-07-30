from graphics import *
from ThreeSpace import *
from math import *

class engine:
    #these must be initialized in constructor
    viewVector = vector(1,1,1)
    yRef = vector(0,0,1)

    def __init__(self, title, dim, fullscreen=False):
        self.pane = GraphWin(title, dim, dim, fullscreen)
        self.pane.setCoords(-dim/2,-dim/2,dim/2,dim/2)
        self.fullx = self.pane.winfo_screenwidth()
        self.fully = self.pane.winfo_screenheight()
        self.yRef = self.project(self.yRef)
        if(fullscreen):
            self.pane.setCoords((-self.fullx)/2,(-self.fully)/2,(self.fullx)/2,(self.fully)/2)

    #returns 3D vector projected onto viewing plane
    def project(self, v):
        if(v.mag()==0):
            return vector(0,0,0)
        k = -dot(self.viewVector,v)/self.viewVector.mag()**2
        n = scalarMult(self.viewVector,k)
        p = add(v,n)
        return p

    def transform(self,p):
        coords = [] #x,y pair
        if(p.mag()==0):
            coords.append([0,0])
            return coords

        val = dot(self.yRef,p)/(self.yRef.mag()*p.mag())
        if(val > 1):#corrects domain produced by rounding error
            val = 1
        elif(val < -1):
            val=-1
        theta = acos(val)

        phi = self.assignRegions(self.yRef, p, theta)

        x = p.mag()*cos(phi)
        y = p.mag()*sin(phi)
        coords.append([x,y])
        return coords

    def assignRegions(self, yRef, p, theta):
        if(self.yRef.x > 0):
            m=(self.yRef.y/self.yRef.x)
            if(p.y>=m*p.x):
                return pi/2 + theta
            elif(p.y<m*p.x):
                return pi/2 - theta
        elif(self.yRef.x < 0):
            m=(self.yRef.y/self.yRef.x)
            if(p.y>=m*p.x):
                return pi/2 - theta
            elif(p.y<m*p.x):
                return pi/2 + theta
        elif(self.yRef.x == 0):
            if(self.yRef.y >= 0):
                if(p.x >= 0):
                    return pi/2 - theta
                elif(p.x < 0):
                    return pi/2 + theta
            elif(self.yRef.y < 0):
                if(p.x >= 0):
                    return pi/2 + theta
                elif(p.x < 0):
                    return pi/2 - theta

    def drawPt(self,win,x,y,color):
        cir = Circle(Point(x,y),3)
        cir.setFill(color)
        cir.draw(win)

    #will draw the selected list of [2D] points onto the pane
    def illustrate(self,coords,color):
        for point in coords:
            self.drawPt(self.pane,point[0],point[1],color)





def vectorGen():
    vectors = []
    for i in range(0,10000):
        v = vector(100*cos(i/20),100*sin(i/20),i)
        vectors.append(v)
    return vectors

def axes(length,engine):
    x = []
    y = []
    z = []
    #axes
    for i in range(-length,length):
        v = vector(0,0,i)
        p = engine.project(v)
        for point in engine.transform(p):
            z.append(point)
    for i in range(-length,length):
        v = vector(0,i,0)
        p = engine.project(v)
        for point in engine.transform(p):
            y.append(point)
    for i in range(-length,length):
        v = vector(i,0,0)
        p = engine.project(v)
        for point in engine.transform(p):
            x.append(point)

    engine.illustrate(x,"blue")
    engine.illustrate(y,"red")
    engine.illustrate(z,"green")

def test():
    e = engine("3DGraphicsEngine",800,True)
    axes(500,e)
    coords = []
    vectors = vectorGen()
    for v in vectors:
        p = e.project(v)
        for point in e.transform(p):
            coords.append(point)

    e.illustrate(coords,"black")
    e.pane.getMouse() #holds focus of screen - click on pane to dismiss and end program
    e.pane.close()

if(__name__ == "__main__"):
    test()
