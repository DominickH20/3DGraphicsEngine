from Engine import *
from math import *
from ThreeSpace import *

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

    def boundingCube(self, size, color):
        x = []
        y = []
        z = []
        half = int(size/2)
        for i in range(-half, half, 10):
            v_one = vector(i, half, half)
            v_two = vector(i,-half, half)
            v_three = vector(i, -half, -half)
            v_four = vector(i, half, -half)
            p_one = self.eng.project(v_one)
            p_two = self.eng.project(v_two)
            p_three = self.eng.project(v_three)
            p_four = self.eng.project(v_four)
            for point in self.eng.transform(p_one):
                x.append(point)
            for point in self.eng.transform(p_two):
                x.append(point)
            for point in self.eng.transform(p_three):
                x.append(point)
            for point in self.eng.transform(p_four):
                x.append(point)
        for i in range(-half,half, 10):
            v_one = vector(half, i, half)
            v_two = vector(-half, i, half)
            v_three = vector(-half, i, -half)
            v_four = vector(half, i, -half)
            p_one = self.eng.project(v_one)
            p_two = self.eng.project(v_two)
            p_three = self.eng.project(v_three)
            p_four = self.eng.project(v_four)
            for point in self.eng.transform(p_one):
                y.append(point)
            for point in self.eng.transform(p_two):
                y.append(point)
            for point in self.eng.transform(p_three):
                y.append(point)
            for point in self.eng.transform(p_four):
                y.append(point)
        for i in range(-half, half, 10):
            v_one = vector(half, half, i)
            v_two = vector(-half, half, i)
            v_three = vector(-half, -half, i)
            v_four = vector(half, -half, i)
            p_one = self.eng.project(v_one)
            p_two = self.eng.project(v_two)
            p_three = self.eng.project(v_three)
            p_four = self.eng.project(v_four)
            for point in self.eng.transform(p_one):
                z.append(point)
            for point in self.eng.transform(p_two):
                z.append(point)
            for point in self.eng.transform(p_three):
                z.append(point)
            for point in self.eng.transform(p_four):
                z.append(point)
        self.eng.illustrate(x, color)
        self.eng.illustrate(y, color)
        self.eng.illustrate(z, color)

    def run(self):
        while True:
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
            self.axes(500)
            self.boundingCube(300, "purple")
            debugmessage = "Debug: "+ "viewVector: "+ str(self.eng.viewVector) +"    "+"q to exit"+"    "+"wasd to move"
            debug = Text(Point(-400,400),debugmessage)
            debug.draw(self.eng.pane)
            update(120)

def test():
    h = engineHost(pi/4,pi/4,engine("HostTest",800,True))
    h.run()

test()
