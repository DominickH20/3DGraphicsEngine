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


    def updateVector(self):
        self.eng.setViewVector(vector(cos(self.theta),sin(self.theta),sin(self.phi)))
        self.eng.setyRef(vector(0,0,1))

    def axes(self,length):
        x = []
        y = []
        z = []
        #axes
        for i in range(-length,length):
            v = vector(0,0,i)
            p = self.eng.project(v)
            for point in self.eng.transform(p):
                z.append(point)
        for i in range(-length,length):
            v = vector(0,i,0)
            p = self.eng.project(v)
            for point in self.eng.transform(p):
                y.append(point)
        for i in range(-length,length):
            v = vector(i,0,0)
            p = self.eng.project(v)
            for point in self.eng.transform(p):
                x.append(point)

        self.eng.illustrate(x,"blue")
        self.eng.illustrate(y,"red")
        self.eng.illustrate(z,"green")

        coords = []
        vectors = []
        for i in range(0,500):
            v = vector(100*cos(i/20),100*sin(i/20),i)
            vectors.append(v)
        for v in vectors:
            p = self.eng.project(v)
            for point in self.eng.transform(p):
                coords.append(point)
        self.eng.illustrate(coords,"black")

    def getPoint(self, coords): ##R3 to R2
        r = []
        v = vector(coords[0],coords[1],coords[2])
        p = self.eng.project(v)
        for point in self.eng.transform(p):
            r.append(point)
        #print(r)
        return r[0]

    def wire(self,a1,a2, color):
        self.eng.drawLine(self.getPoint(a1)[0],self.getPoint(a1)[1],self.getPoint(a2)[0],self.getPoint(a2)[1], color)

    def renderAxes(self,vertices):
        self.wire(vertices[0],vertices[3],"red")
        self.wire(vertices[1], vertices[3], "green")
        self.wire(vertices[2], vertices[3], "blue")

    def renderLattice(self,vertices):
        size = vertices[0][0]
        print(size)
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

    def run(self):
        hostX = self.eng.fullx
        hostY = self.eng.fully
        hostName = self.eng.title
        frame = 0
        delta = []
        fps = 0
        a = axes(300)
        l = lattice(400, -100)
        wc = wireCube(0,0,100,50, "brown")
        while True:
            start = time.time()
            key = self.eng.pane.checkKey()
            if (key == "w"):
                if(self.phi < pi/2):
                    self.phi += pi/64
                #self.eng.pane.delete("all")
            if (key == "a"):
                self.theta -= pi/64
                #self.eng.pane.delete("all")
            if (key == "s"):
                if(self.phi > -pi/2):
                    self.phi -= pi/64
                #self.eng.pane.delete("all")
            if (key == "d"):
                self.theta += pi/64
                #self.eng.pane.delete("all")
            if (key == "q"):
                self.eng.pane.close()
                break
            self.eng.pane.delete("all")
            self.updateVector()
            ######OBJECT TRANSFORMATIONS IF ANY######

            ######RENDERING#######
            for obj in WorldObjects.getinstances():
                if(isinstance(obj,lattice)):
                    self.renderLattice(obj.vertices)
                if(isinstance(obj, wireCube)):
                    self.renderWireCube(obj.vertices, obj.color)
                if(isinstance(obj,axes)):
                    self.renderAxes(obj.vertices)
            ######DEBUG#######
            debugmessage = "Running" + " " + hostName + " " + "(" + format(fps, '03f')+ " fps" + ")" + " " + "\n"+"viewX: "+ format(self.eng.viewVector.x, '02f')+"\n"+"viewY: "+ format(self.eng.viewVector.y, '02f')+"\n"+"viewZ: "+ format(self.eng.viewVector.z, '02f')
            #debugmessage = "Debug: "+ "viewVector: "+ str(self.eng.viewVector) +"    "+"q to exit"+"    "+"wasd to move"
            debug = Text(Point((-hostX/3),(hostY)/4),debugmessage)
            debug.draw(self.eng.pane)
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
