from graphics import *

class engine:

    def __init__(self, title, dim):
        self.pane = GraphWin(title, dim, dim)
        self.pane.setCoords(-dim/2,-dim/2,dim/2,dim/2)

    def drawPt(self,win,x,y):
        cir = Circle(Point(x,y),5)
        cir.setFill("black")
        cir.draw(win)

    #will draw the selected list of [2D] points onto the pane
    def illustrate(self,coords):
        for point in coords:
            self.drawPt(self.pane,point[0],point[1])


def main():
    e = engine("3DGraphicsEngine",800)
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
