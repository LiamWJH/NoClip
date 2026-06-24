import pygame
import noclip

noclip.initialize((1280, 720))

def setupgame():
    global basespace
    basespace = noclip.space_001
    img = noclip.loadimage("assets/bacteria.webp")
    x = noclip.centerX(basespace.width, img.width)
    y = noclip.centerY(basespace.height, img.height)
    basespace.newchild(noclip.thing("shit2", (0, 0), None))
    basespace.newchild(noclip.thing("shit", (x, y), img))


def update():
    s = basespace.returnchild("shit")
    s.x = noclip.centerX(basespace.width, s.width)
    s.y = noclip.centerY(basespace.height, s.height)

noclip.run(setupgame, update)
