import pygame
import noclip

noclip.initialize((1280, 720))

def setupgame():
    global basespace
    basespace = noclip.space_001
    noclip.assets.image("backrooms", fileformat="jpg")
    noclip.assets.image("bacteria", fileformat="png")
    noclip.assets.sound("fah", fileformat="mp3")
    x = noclip.centerX(basespace.width, noclip.assets.image("backrooms").width)
    y = noclip.centerY(basespace.height, noclip.assets.image("bacteria").height)
    basespace.newchild(noclip.thing("shit2", (x, y), noclip.assets.image("bacteria")))
    basespace.returnchild("shit2").add_timer("flasheffect")
    basespace.newchild(noclip.thing("shit", (x, y), noclip.assets.image("backrooms")))

    def shit2_update(self):
        self.timer["flasheffect"] += noclip.dt
        if self.timer["flasheffect"] > 0.3:
            noclip.switchbig("shit")
            self.timer["flasheffect"] = 0

    basespace.returnchild("shit2").update = shit2_update
    noclip.switchbig("shit")

def update():
    if noclip.keyJustPressed("space"):
        noclip.switchbig("shit2")
        noclip.assets.sound("fah", volume=0.01).play()
    if noclip.keyPressed("right"):
        noclip.camera.move_view_xy((90, 3))
    if noclip.keyPressed("left"):
        noclip.camera.move_view_xy((-90, 3))
    if noclip.keyPressed("down"):
        noclip.camera.move_view_z(0.01)
noclip.run(setupgame, update)
