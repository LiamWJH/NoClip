import pygame
import noclip

noclip.initialize((1280, 720))

def setupgame():
    global basespace
    basespace = noclip.space_001
    img = noclip.setopacity(noclip.loadimage("assets/backrooms.jpg"), 100)
    img2 = noclip.setopacity(noclip.loadimage("assets/bacteria.png"), 20)
    x = noclip.centerX(basespace.width, img.width)
    y = noclip.centerY(basespace.height, img.height)
    basespace.newchild(noclip.thing("shit2", (x, y), img2))
    basespace.returnchild("shit2").add_timer("flasheffect")
    basespace.newchild(noclip.thing("shit", (x, y), img))

    def shit2_update(self):
        self.timer["flasheffect"] += noclip.dt
        if self.timer["flasheffect"] > 0.3:
            noclip.switchbig("shit")
            self.timer["flasheffect"] = 0

    basespace.returnchild("shit2").update = shit2_update
    noclip.switchbig("shit")

def update():
    if noclip.keyPressed("space"):
        noclip.switchbig("shit2")
    if noclip.keyPressed("right"):
        noclip.camera.move_view_xy((90, 3))
    if noclip.keyPressed("left"):
        noclip.camera.move_view_xy((-90, 3))
    if noclip.keyPressed("down"):
        noclip.camera.move_view_z(0.01)
noclip.run(setupgame, update)
