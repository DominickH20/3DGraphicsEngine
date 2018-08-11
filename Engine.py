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
        self.title = title
        if(fullscreen):
            self.pane.setCoords((-self.fullx)/2,(-self.fully)/2,(self.fullx)/2,(self.fully)/2)

    def setViewVector(self,vec):
        self.viewVector = vec

    def getyRef(self):
        return self.yRef

    def setyRef(self,vec):
        self.yRef = self.project(vec)

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
        cir.setOutline(color)
        cir.draw(win)

    def drawLine(self,x1,y1,x2,y2, color = "black"):
        line = Line(Point(x1,y1),Point(x2,y2), color)
        line.draw(self.pane)

    #will draw the selected list of [2D] points onto the pane
    def illustrate(self,coords,color):
        for point in coords:
            self.drawPt(self.pane,point[0],point[1],color)

