from Engine import *
from math import *
from ThreeSpace import *
from WorldObjects import *
import time
import gc

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
        hostX = self.eng.fullx
        hostY = self.eng.fully
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
    #ideally we want to remove frame as an input for this method
    def render(self,frame):
        a = axes(300)
        l = lattice(400, -100)
        h = helix(100, 0, 250, 20, 5, 10, "purple")
        wc = wireCube(0,0,100,50, "brown")

        ######OBJECT TRANSFORMATIONS IF ANY######
        h.updateVertices(100, 0, 250, 20, int((frame/15))+1, 10, "purple")
        ######RENDERING#######
        for obj in WorldObjects.getinstances():
            if(isinstance(obj,lattice)):
                self.renderLattice(obj.vertices)
            if(isinstance(obj, wireCube)):
                self.renderWireCube(obj.vertices, obj.color)
            if (isinstance(obj, helix)):
                self.renderHelix(obj.vertices, obj.color)
            if(isinstance(obj,axes)):
                self.renderAxes(obj.vertices)

    #method to handle debug message view - ideally want to decrease number of vars in function
    def printDebug(self,fps):
        hostX = self.eng.fullx
        hostY = self.eng.fully
        hostName = self.eng.title
        ######DEBUG#######
        debugmessage = "Running" + " " + hostName + " "
        debugmessage += "(" + format(fps, '03f')+ " fps" + ")"
        debugmessage += " " + "\n"+"viewX: "+ format(self.eng.viewVector.getX(), '02f')
        debugmessage += " " + "\n"+"viewY: "+ format(self.eng.viewVector.getY(), '02f')
        debugmessage += " " + "\n"+"viewZ: "+ format(self.eng.viewVector.getZ(), '02f')
        debugmessage += " " + "\n"+"Magnification (z/x): " + format(self.eng.getZoom(),'02f')
        debugmessage += " " + "\n"+"xTraversal (j/l): " + format(self.eng.getxTraversal(),'05d')
        debugmessage += " " + "\n" + "yTraversal (i/k): " + format(self.eng.getyTraversal(), '05d')

        debug = Text(Point((-hostX/3),(hostY)/4),debugmessage)
        debug.draw(self.eng.pane)


    #core loop that produces rendering and takes user input
    #want to remove local variables and handle fps better - this should be a clean function
    def run(self):
        frame = 0
        delta = []
        fps = 0
        zoom = 1

        while True:
            start = time.time()
            if(self.handleKeys(self.eng.pane.checkKey())):
                break;

            self.eng.pane.delete("all")
            self.updateVector()
            self.render(frame)
            self.printDebug(fps)
            update(120)

            frame +=1
            end = time.time()
            diff = end-start
            delta.append(diff)
            if(frame % 10 ==0):
                fps = 1/(sum(delta)/len(delta))
                delta = []

def main():
    h = engineHost(pi/4,pi/4,engine("Host",800,True))
    h.run()

main()
