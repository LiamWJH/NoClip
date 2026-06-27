import pygame
import noclip

noclip.initialize((1280, 720))

def setupgame():
    global basespace
    basespace = noclip.space_001
    img = noclip.setopacity(noclip.loadimage("assets/bacteria.png"), 100)
    img2 = noclip.setopacity(noclip.loadimage("assets/backrooms.jpg"), 80)
    x = noclip.centerX(basespace.width, img.width)
    y = noclip.centerY(basespace.height, img.height)
    basespace.newchild(noclip.thing("shit2", (x, y), img2))
    basespace.newchild(noclip.thing("shit", (x, y), img))
    noclip.switchbig("shit")


def update():
    if noclip.keyPressed("space"):
        noclip.switchbig("shit2")

noclip.run(setupgame, update)
