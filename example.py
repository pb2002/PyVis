import piefish as pv

pv.init()


@pv.kernel.pool("setup", 1)
def start():
    pv.framerate(120)
    pv.size(1280, 720)
    #pv.fullscreen()
    pv.kernel.log("hello, this method was called from the setup pool!", 4)


# this layer gets drawn first because it has a higher priority level
@pv.kernel.pool("draw", 1)
def layer1():
    pv.background(0, 16, 32)

    pv.fill(0, 24, 48)
    pv.noStroke()
    pv.circle(pv.width // 2, pv.height // 2, pv.height // 2 - 50)


@pv.kernel.pool("draw", 2)
def layer2():
    offset = (pv.width - 700) // 2
    pv.fill(255, 32, 96)
    pv.stroke(255)
    pv.strokeWeight(2)

    pv.rect(offset + 10, 10, 80, 80)
    pv.ellipse(offset + 110, 10, 180, 80)
    pv.circle(offset + 350, 50, 40)
    pv.polygon([(offset + 410, 10), (offset + 490, 10), (offset + 450, 90)])
    pv.line(offset + 510, 10, offset + 590, 90, False)
    pv.line(offset + 610, 10, offset + 690, 90, True)

    pv.fill(32, 225, 255)
    pv.stroke(192)
    pv.strokeWeight(1)

    pv.line(offset + 10, 120, offset + 690, 120, False)

    pv.font('Montserrat', 48, True)
    pv.label(pv.width // 2, 120, 'PyVis Example App', centered=True)
    pv.font('Montserrat', 18, False)
    pv.label(15, 15, "FPS: {0:0.2f}".format(pv.kernel.capped_framerate), centered=False)
    pv.label(15, 45, "Potential FPS: {0:0.2f}".format(pv.kernel.potential_framerate), centered=False)

pv.kernel.run()
