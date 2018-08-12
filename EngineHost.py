from Engine import *
from math import *
from ThreeSpace import *
import time

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

        #coords = []
        #vectors = []
        #for i in range(0,500):
        #    v = vector(100*cos(i/20),100*sin(i/20),i)
        #    vectors.append(v)
        #for v in vectors:
        #    p = self.eng.project(v)
        #    for point in self.eng.transform(p):
        #        coords.append(point)
        #
        #self.eng.illustrate(coords,"black")

    def run(self):
        hostX = self.eng.fullx
        hostY = self.eng.fully
        hostName = self.eng.title
        frame = 0
        delta = []
        fps = 0
        while True:
            start = time.time()
            key = self.eng.pane.checkKey()
            if (key == "w"):
                if(self.phi < pi/2):
                    self.phi += pi/64
                self.eng.pane.delete("all")
            if (key == "a"):
                self.theta -= pi/64
                self.eng.pane.delete("all")
            if (key == "s"):
                if(self.phi > -pi/2):
                    self.phi -= pi/64
                self.eng.pane.delete("all")
            if (key == "d"):
                self.theta += pi/64
                self.eng.pane.delete("all")
            if (key == "q"):
                self.eng.pane.close()
                break
            self.updateVector()

            self.eng.pane.delete("all")
            self.axes(500)
            debugmessage = "Running" + " " + hostName + " " + "(" + format(fps, '03f')+ " fps" + ")" + " " + "\n"+"viewX: "+ format(self.eng.viewVector.x, '02f')+"\n"+"viewY: "+format(self.eng.viewVector.y, '02f')+"\n"+"viewZ: "+ format(self.eng.viewVector.z, '02f')
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
