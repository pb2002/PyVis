from pyvis import *

pyvis_init()

@kernel.pool("setup", 1)
def start():
    frameRate(1000)
    size(800,800)
    print("hello, this method was called from the setup pool!")

@kernel.pool("draw", 1) # this layer gets drawn first because it has a higher priority level
def layer1():
    background(0,16,32)
    fill(0,24,48)
    noStroke()
    circle(400,400,380)

i = 0
@kernel.pool("draw", 2)
def layer2():
    global i
    i += 1
    fill(255,32,96)
    stroke(255)
    strokeWeight(2)

    rect(60,10,80,80)
    ellipse(160,10,180,80)
    circle(400,50,40)
    polygon([(460,10),(540,10),(500,90)])
    line(560,10,640,90,False)
    line(660,10,740,90,True)
    
    fill(32,225,255)
    stroke(192)
    strokeWeight(1)
    if(i > 500):
        print(kernel.current_fps)
        i = 0
#    line(70,120,730,120,False)
#    font('Segoe UI',48,True)
#    label(180,120,'PyVis Example App')
#    font('Segoe UI',24,False)
#    label(180,200,"FPS: {0:0.2f}".format(kernel.current_fps))
kernel.run()