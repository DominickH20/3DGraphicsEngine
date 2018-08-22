from Engine import *
from math import *
from ThreeSpace import *
from WorldObjects import *
import time
import copy

class engineHost:
    theta = pi/4
    phi = pi/4
    eng = None

    def __init__(self,theta,phi,eng):
        self.theta = theta
        self.phi = phi
        self.eng = eng

    #updates the the engine projection vectors based on input data from host
    def updateVector(self):
        self.eng.setViewVector(vector(cos(self.theta),sin(self.theta),sin(self.phi)))
        self.eng.setyRef(vector(0,0,1)) #no use yet - revolution is not implemented

    #depth score calculations
    def normViewVector(self):
        return normalize(self.eng.getviewVector())

    def avgdepth(self, coords):
        depths = []
        #print(coords)
        for point in coords:
            #dist to cam plane
            x = point[0]
            y = point[1]
            z = point[2]
            #print((x*self.normViewVector().x+y*self.normViewVector().y+z*self.normViewVector().z+500))
            score = (x*self.normViewVector().x+y*self.normViewVector().y+z*self.normViewVector().z+500)
            #print(score)
            depths.append(int(score))
            #depths.append((x*int(self.normViewVector().x)+y*int(self.normViewVector().y)+z*int(self.normViewVector().z)+500)/7)
        return sum(depths)/len(depths)

    #lightingscorecalculations
    def getlightFactor(self,p1,p2,p3):
        light = vector(0.282,0.929,0.236)
        v1 = vector(p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2])
        v2 = vector(p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])
        normal = cross(v1,v2)
        unitnorm = normalize(normal)
        dotted = dot(light,unitnorm)
        return int(20*dotted) #temporary


    #retrieves appropriate drawing coordinates from a specified point in R3
    def getPoint(self, point):
        v = vector(point[0],point[1],point[2])
        p = self.eng.project(v)
        r = self.eng.transform(p)
        return r

    #draws line between two given points p1 and p2
    def wire(self,p1,p2,color):
        self.eng.drawLine(self.getPoint(p1)[0],self.getPoint(p1)[1],self.getPoint(p2)[0],self.getPoint(p2)[1], color)

    def renderAxes(self,vertices):
        self.wire(vertices[0],vertices[3],"red")
        self.wire(vertices[1], vertices[3], "green")
        self.wire(vertices[2], vertices[3], "blue")

    def renderLattice(self,vertices):
        size = vertices[0][0]
        #print(size)
        zlevel = vertices[0][2]
        for i in range(-size,size,60):
            self.wire([i,-size,zlevel],[i,size,zlevel],"lightblue")
            self.wire([-size, i, zlevel], [size, i, zlevel], "lightblue")

    def renderWireCube(self, vertices, color):
        self.wire(vertices[0],vertices[1], color)
        self.wire(vertices[1], vertices[3], color)
        self.wire(vertices[3], vertices[2], color)
        self.wire(vertices[2], vertices[0], color)
        self.wire(vertices[4], vertices[5], color)
        self.wire(vertices[5], vertices[7], color)
        self.wire(vertices[7], vertices[6], color)
        self.wire(vertices[6], vertices[4], color)
        self.wire(vertices[0], vertices[4], color)
        self.wire(vertices[1], vertices[5], color)
        self.wire(vertices[2], vertices[6], color)
        self.wire(vertices[3], vertices[7], color)

    def renderHelix(self, vertices, color):
        v = 0
        while v < len(vertices)-1:
            self.wire(vertices[v],vertices[v+1],color)
            v+=1

    #handles value assignment when keys are pressed. T/F indicates when to break out of loop
    def handleKeys(self,key):
        if (key == "q"):
            self.eng.pane.close()
            return True
        else:
            if (key == "w"):
                if(self.phi < pi/2):
                    self.phi += pi/64
            if (key == "a"):
                self.theta -= pi/64
            if (key == "s"):
                if(self.phi > -pi/2):
                    self.phi -= pi/64
            if (key == "d"):
                self.theta += pi/64
            if (key == "z"):
                self.eng.zoomIn()
            if (key == "x"):
                self.eng.zoomOut()
            if (key == "j"):
                self.eng.traverseLeft()
            if (key == "l"):
                self.eng.traverseRight()
            if (key == "i"):
                self.eng.traverseUp()
            if (key == "k"):
                self.eng.traverseDown()
            return False

    #method to handle object rendering - ALL RENDERING MUST BE DONE HERE
    def render(self):
        renderMesh = copy.deepcopy(WorldObjects.globalMesh) #deepcopy to preserve globalMesh
        for polygon in renderMesh:
            polygon.append(self.avgdepth(polygon[0]))
        #sort by depth score
        renderMesh = sorted(renderMesh, key = lambda x: x[-1], reverse = False)
        #draw globalmesh
        for polygon in renderMesh:
            r2points = []
            for r3point in polygon[0]:
                r2points.append(self.getPoint(r3point))
            r2pointsfinal = []
            for pair in r2points:
                r2pointsfinal.append(Point(pair[0],pair[1]))
            #grayscale shading
            if(polygon[1]==color_rgb(127,127,127)):
                lightFactor = self.getlightFactor(polygon[0][0],polygon[0][1],polygon[0][2])
                shade = color_rgb(127+lightFactor,127+lightFactor,127+lightFactor)
                self.eng.drawPoly(r2pointsfinal,shade)
            else:
                self.eng.drawPoly(r2pointsfinal, polygon[1])
        #draw axes
        for obj in WorldObjects.getinstances():
            #if(isinstance(obj,lattice)):
            #    self.renderLattice(obj.vertices)
            #if(isinstance(obj, wireCube)):
            #    self.renderWireCube(obj.vertices, obj.color)
            #if (isinstance(obj, helix)):
            #    self.renderHelix(obj.vertices, obj.color)
            if(isinstance(obj,axes)):
                self.renderAxes(obj.vertices)
        #print(renderMesh)
        #self.eng.drawPoly([Point(0,50), Point(50,50),Point(50,0), Point(0,0)],color_rgb(90,50,50))
        #self.eng.drawPoly([Point(50, 0), Point(100, 0), Point(100, 50), Point(50, 50)], color_rgb(int(90*1.2), int(50*1.2), int(50*1.2)))
        #self.eng.drawPoly([self.eng.pane.Point(0,0), Point(-10,20),Point(-30,500)])

    #method to handle debug message view - ideally want to decrease number of vars in function
    def printDebug(self,fpsHandler):
        ######DEBUG#######
        debugmessage = "Running" + " " + self.eng.title + " "
        debugmessage += "(" + format(fpsHandler.getFPS(), '03f')+ " fps" + ")"
        debugmessage += " " + "\n"+"viewX: "+ format(self.eng.viewVector.getX(), '02f')
        debugmessage += " " + "\n"+"viewY: "+ format(self.eng.viewVector.getY(), '02f')
        debugmessage += " " + "\n"+"viewZ: "+ format(self.eng.viewVector.getZ(), '02f')
        #debugmessage += " " + "\n"+"normViewVector: " + str(self.normViewVector())
        debugmessage += " " + "\n"+"Magnification (z/x): " + format(self.eng.getZoom(),'02f')
        debugmessage += " " + "\n"+"xTraversal (j/l): " + format(self.eng.getxTraversal(),'05d')
        debugmessage += " " + "\n" + "yTraversal (i/k): " + format(self.eng.getyTraversal(), '05d')

        debug = Text(Point((-self.eng.xDist/3),(self.eng.yDist)/4),debugmessage)
        debug.draw(self.eng.pane)


    #core loop that produces rendering and takes user input
    #want to remove local variables and handle fps better - this should be a clean function
    def run(self):
        fpsHandler = FPSHandler()
        #####OBJECT INITIALIZATION ALWAYS HERE----DO NOT PUT IN RENDER####
        a = axes(300)
        #p = flatPlane(200, -70, "white")
        cub = cube(100, 0,0,40, color_rgb(127,127,127))
        other = cube(50,-300,70,90, color_rgb(127,127,127))
        while True:
            fpsHandler.timeStamp()
            if(self.handleKeys(self.eng.pane.checkKey())):
                break;
            self.eng.pane.delete("all")
            self.updateVector()
            self.render()
            fpsHandler.update()
            self.printDebug(fpsHandler)
            update(120)
            #print(self.normViewVector())


class FPSHandler:

    def __init__(self):
        self.frame = 0
        self.delta=[]
        self.fps = 0

    def getFPS(self):
        return self.fps

    def timeStamp(self):
        self.start = time.time()

    def update(self):
        self.frame +=1
        self.end = time.time()
        diff = self.end-self.start
        self.delta.append(diff)
        if(self.frame % 10 == 0):
            self.fps = 1/(sum(self.delta)/len(self.delta))
            self.delta = []

def main():
    h = engineHost(pi/4,pi/4,engine("Host",800,True))
    h.run()

main()
