from Engine import *

def animationdemo():
    e = engine("Animation_Demo",500)
    xpos=0
    ypos=0
    while True:
        key = e.pane.checkKey()
        if (key == "w"):
            ypos += 5
            e.pane.delete("all")
        if (key == "a"):
            xpos -= 5
            e.pane.delete("all")
        if (key == "s"):
            ypos -= 5
            e.pane.delete("all")
        if (key == "d"):
            xpos += 5
            e.pane.delete("all")
        if (key == "q"):
            e.pane.close()
            break
        e.drawPt(e.pane,xpos,ypos,"black")
        debugmessage = "Debug: "+"x_pos: "+format(xpos, '05d')+"   "+"y_pos: "+format(ypos, '05d')+"    "+"q to exit"+"    "+"wasd to move"
        debug = Text(Point(-10,210),debugmessage)
        debug.draw(e.pane)
        update(120)

animationdemo()