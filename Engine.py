from graphics import *
from ThreeSpace import *
from math import *

class engine:

    viewVector = vector(1,1,1)

    def __init__(self, title, dim, fullscreen=False):
        self.pane = GraphWin(title, dim, dim, fullscreen)
        self.pane.setCoords(-dim/2,-dim/2,dim/2,dim/2)
        self.fullx = self.pane.winfo_screenwidth()
        self.fully = self.pane.winfo_screenheight()
        if(fullscreen):
            self.pane.setCoords((-self.fullx)/2,(-self.fully)/2,(self.fullx)/2,(self.fully)/2)

    #returns 3D vector projected onto viewing plane
    def project(self, v):
        if(v.mag()==0):
            return vector(0,0,0)
        #be aware of when dot product returns 0
        k = -dot(self.viewVector,v)/self.viewVector.mag()**2
        #print(k)
        n = scalarMult(self.viewVector,k)
        #print(n)
        p = add(v,n)
        #print(p)
        return p

    #ensure magnitudes are > 0, make sure acos has proper domain
    def transform(self,p):
        coords = [] #x,y pair
        if(p.mag()==0):
            coords.append([0,0])
            return coords

        kp = self.project(vector(0,0,1))
        #print(kp)
        val = dot(kp,p)/(kp.mag()*p.mag())
        if(val > 1):#corrects domain produced by rounding error
            #print(val)
            val = 1
        elif(val < -1):
            #print(val)
            val=-1
        theta = acos(val)

        #assign regions - limiting with kp as y axis
        #add further region classification
        m=(kp.y/kp.x) #ensure kp.x != 0
        if(p.y>=m*p.x):
            #right side
            phi = pi/2 - theta
        elif(p.y<m*p.x):
            #left side
            phi = pi/2 + theta

        x = p.mag()*cos(phi)
        y = p.mag()*sin(phi)
        coords.append([x,y])
        return coords



    def drawPt(self,win,x,y):
        cir = Circle(Point(x,y),5)
        cir.setFill("black")
        cir.draw(win)

    #will draw the selected list of [2D] points onto the pane
    def illustrate(self,coords):
        for point in coords:
            self.drawPt(self.pane,point[0],point[1])

def vectorGen():
    vectors = []
    for i in range(0,10000):
        v = vector(100*cos(i/20),100*sin(i/20),i)
        vectors.append(v)
    return vectors

def test():
    e = engine("3DGraphicsEngine",800,True)
    coords = []
    #axes
    for i in range(1,500):
        v = vector(0,0,i)
        p = e.project(v)
        for point in e.transform(p):
            coords.append(point)
    for i in range(1,500):
        v = vector(0,i,0)
        p = e.project(v)
        for point in e.transform(p):
            coords.append(point)
    for i in range(1,500):
        v = vector(i,0,0)
        p = e.project(v)
        for point in e.transform(p):
            coords.append(point)

    vectors = vectorGen()
    for v in vectors:
        p = e.project(v)
        for point in e.transform(p):
            coords.append(point)


    e.illustrate(coords)
    e.pane.getMouse() #holds focus of screen - click on pane to dismiss and end program
    e.pane.close()

test()
