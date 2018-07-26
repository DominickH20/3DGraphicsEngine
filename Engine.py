from graphics import *

class engine:

    def __init__(self, title, dim, fullscreen=False):
        self.pane = GraphWin(title, dim, dim, fullscreen)
        self.pane.setCoords(-dim/2,-dim/2,dim/2,dim/2)
        self.fullx = self.pane.winfo_screenwidth()
        self.fully = self.pane.winfo_screenheight()
        if(fullscreen):
            self.pane.setCoords((-self.fullx)/2,(-self.fully)/2,(self.fullx)/2,(self.fully)/2)

    def drawPt(self,win,x,y):
        cir = Circle(Point(x,y),5)
        cir.setFill("black")
        cir.draw(win)

    #will draw the selected list of [2D] points onto the pane
    def illustrate(self,coords):
        for point in coords:
            self.drawPt(self.pane,point[0],point[1])


def main():
<<<<<<< HEAD
    e = engine("3DGraphicsEngine",800,True)
=======
    e = engine("3DGraphicsEngine",800, True)
>>>>>>> e9182d6ae106d51b66c71f6d768124e54ef192ba
    coords = []
    for i in range(0,300):
        coords.append([0,i])
    e.illustrate(coords)
    coords = []
    for i in range(0,300):
        coords.append([i,0])
    e.illustrate(coords)
    e.pane.getMouse() #holds focus of screen - click on pane to dismiss and end program
    e.pane.close()

main()
