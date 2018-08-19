from graphics import *
from ThreeSpace import *
from math import *

class engine:
    #these must be initialized in constructor
    viewVector = vector(1,1,1)
    yRef = vector(0,0,1)

    zoom = 1
    xTraversal = 0
    yTraversal = 0

    def __init__(self, title, dim, fullscreen=False):
        self.pane = GraphWin(title, dim, dim, fullscreen)
        self.yRef = self.project(self.yRef)
        self.title = title

        self.xDist = dim
        self.yDist = dim
        self.pane.setCoords(-dim/2,-dim/2,dim/2,dim/2)
        if(fullscreen):
            self.xDist = self.pane.winfo_screenwidth()
            self.yDist = self.pane.winfo_screenheight()
            self.pane.setCoords((-self.xDist)/2,(-self.yDist)/2,(self.xDist)/2,(self.yDist)/2)

    #accessors and mutators
    def getviewVector(self):
        return self.viewVector

    def setViewVector(self,vec):
        self.viewVector = vec

    def getyRef(self):
        return self.yRef

    def setyRef(self,vec):
        self.yRef = self.project(vec)

    #view magnification
    def zoomIn(self):
        self.zoom += 0.01

    def zoomOut(self):
        self.zoom -= 0.01

    def getZoom(self):
        return self.zoom

    #Linear camera tracking

    def traverseLeft(self):
        self.xTraversal -= 5

    def traverseRight(self):
        self.xTraversal += 5

    def traverseUp(self):
        self.yTraversal += 5

    def traverseDown(self):
        self.yTraversal -= 5

    def getxTraversal(self):
        return self.xTraversal

    def getyTraversal(self):
        return self.yTraversal

    #returns 3D vector projected onto viewing plane
    def project(self, v):
        if(v.mag()==0):
            return vector(0,0,0)
        k = -dot(self.viewVector,v)/self.viewVector.mag()**2
        n = scalarMult(self.viewVector,k)
        p = add(v,n)
        return p

    #returns a pair x,y of points representing a projected vector's position on the screen
    #the returned list has x=list[0] and y = list[1]
    def transform(self,p):
        pair = [] #x,y pair
        if(p.mag()==0):
            x=0 + self.xTraversal
            y=0 + self.yTraversal
            pair.append(x)
            pair.append(y)
            return pair

        val = dot(self.yRef,p)/(self.yRef.mag()*p.mag())
        if(val > 1):#corrects domain produced by rounding error
            val = 1
        elif(val < -1):#analogous correction
            val=-1
        theta = acos(val)

        phi = self.assignRegions(p, theta)

        x = p.mag()*cos(phi)*self.zoom + self.xTraversal
        y = p.mag()*sin(phi)*self.zoom + self.yTraversal

        if(self.viewVector.z<0):#reflection bug fix
            x = -x + self.xTraversal*2 #Displace to account for negative z after traversal
        pair.append(x)
        pair.append(y)
        return pair

    #determines on which side of the window to display points
    def assignRegions(self, p, theta):
        if (self.yRef.x > 0):
            m = (self.yRef.y / self.yRef.x)
            if (p.y >= m * p.x):
                return pi / 2 + theta
            elif (p.y < m * p.x):
                return pi / 2 - theta
        elif (self.yRef.x < 0):
            m = (self.yRef.y / self.yRef.x)
            if (p.y >= m * p.x):
                return pi / 2 - theta
            elif (p.y < m * p.x):
                return pi / 2 + theta
        elif (self.yRef.x == 0):
            if (self.yRef.y >= 0):
                if (p.x >= 0):
                    return pi / 2 - theta
                elif (p.x < 0):
                    return pi / 2 + theta
            elif (self.yRef.y < 0):
                if (p.x >= 0):
                    return pi / 2 + theta
                elif (p.x < 0):
                    return pi / 2 - theta

    #POOR PERFORMANCE - DO NOT USE
    def drawPt(self,win,x,y,color):
        cir = Circle(Point(x,y),3)
        cir.setFill(color)
        cir.setOutline(color)
        cir.draw(win)

    #draws a line connecting two points on the viewing plane
    def drawLine(self,x1,y1,x2,y2, color):
        line = Line(Point(x1,y1),Point(x2,y2), color)
        line.draw(self.pane)

    #POOR PERFORMANCE - DO NOT USE
    #will draw the selected list of [2D] points onto the pane
    def illustrate(self,coords,color):
        for point in coords:
            self.drawPt(self.pane,point[0],point[1],color)
