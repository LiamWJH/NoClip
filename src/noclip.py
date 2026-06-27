import pygame
import os

screen = None
clock = None
dt = 0
running = True


class Err(Exception):
    def __init__(self, err, msg):
        self.err = err
        self.msg = msg
    def show(self):
        print(f"{self.__class__.__name__} Error: \n'{self.err}': {self.msg}")

class NoExistError(Err): pass

class thing:
    def __init__(self, name, coords, shape):
        self.name = name
        self.x, self.y = coords
        self.shape = shape
        self.width, self.height = self.size()
        self.children = []

    def size(self):
        if self.shape is None:
            return (32, 32)
        return self.shape.get_size()

    def setsize(self, w, h):
        self.width, self.height = w, h

    def AABB(self):
        x2 = self.x + self.width
        y2 = self.y + self.height
        return {"x1": self.x, "x2": x2, "y1": self.y, "y2": y2}

    def overlapswith(self, t):
        a = self.AABB()
        b = t.AABB()
        return (
            a["x1"] < b["x2"] and
            a["x2"] > b["x1"] and
            a["y1"] < b["y2"] and
            a["y2"] > b["y1"]
        )

    def newchild(self, child: "thing"):
        self.children.append(child)

    def returnchild(self, path):
        parts = path.split("/", 1)
        head = parts[0]
        found = None
        for child in self.children:
            if child.name == head:
                found = child
                break
        if found is None:
            raise NoExistError(f"no child named '{head}' found", "Maybe you typed it wrong or didnt make the class yet...")
        if len(parts) == 1:
            return found
        return found.returnchild(parts[1])


def centerX(w1, w2):
    return w1 / 2 - w2 / 2
def centerY(h1, h2):
    return h1 / 2 - h2 / 2


space_001 = thing("space-001", (0, 0), None)

KEY_MAP = {
    "`": pygame.K_BACKQUOTE,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,
    "0": pygame.K_0,
    "-": pygame.K_MINUS,
    "=": pygame.K_EQUALS,
    "backspace": pygame.K_BACKSPACE,
    "tab": pygame.K_TAB,
    "q": pygame.K_q,
    "w": pygame.K_w,
    "e": pygame.K_e,
    "r": pygame.K_r,
    "t": pygame.K_t,
    "y": pygame.K_y,
    "u": pygame.K_u,
    "i": pygame.K_i,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "[": pygame.K_LEFTBRACKET,
    "]": pygame.K_RIGHTBRACKET,
    "\\": pygame.K_BACKSLASH,
    "capslock": pygame.K_CAPSLOCK,
    "a": pygame.K_a,
    "s": pygame.K_s,
    "d": pygame.K_d,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    ";": pygame.K_SEMICOLON,
    "'": pygame.K_QUOTE,
    "enter": pygame.K_RETURN,
    "leftshift": pygame.K_LSHIFT,
    "rightshift": pygame.K_RSHIFT,
    "z": pygame.K_z,
    "x": pygame.K_x,
    "c": pygame.K_c,
    "v": pygame.K_v,
    "b": pygame.K_b,
    "n": pygame.K_n,
    "m": pygame.K_m,
    ",": pygame.K_COMMA,
    ".": pygame.K_PERIOD,
    "/": pygame.K_SLASH,
    "leftctrl": pygame.K_LCTRL,
    "rightctrl": pygame.K_RCTRL,
    "leftalt": pygame.K_LALT,
    "rightalt": pygame.K_RALT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "space": pygame.K_SPACE,
    "escape": pygame.K_ESCAPE,
}
bigthing = space_001


def switchbig(path):
    global bigthing
    bigthing = space_001.returnchild(path)

def initialize(dimension) -> None:
    global screen, clock, dt, running
    width, height = dimension
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    space_001.setsize(*screen.get_size())
    clock = pygame.time.Clock()
    dt = 0
    running = True

def didQuit() -> bool:
    global running
    global screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            space_001.setsize(event.w, event.h)
    return running


def internalsetupgame(setupgame) -> None:
    setupgame()

def setupgame() -> None:
    pass


def internalupdategame(logic) -> None:
    bigthing.x = centerX(space_001.width, bigthing.width)
    bigthing.y = centerY(space_001.height, bigthing.height)
    logic()

def updategame() -> None:
    pass


def blitthing(t, parent) -> None:
    abs_x = parent.x + t.x
    abs_y = parent.y + t.y
    if t.shape == None:
        print("missing texture at", abs_x, abs_y)
        screen.blit(setopacity(loadimage("internal_assets/missing_texture.jpg"), 10), (abs_x, abs_y))
    else:
        screen.blit(t.shape, (abs_x, abs_y))

    for child in t.children:
        blitthing(child, t)

def internaldrawgame(draw) -> None:
    screen.fill((255, 255, 255))
    draw()
    blitthing(bigthing, space_001)

def drawgame() -> None:
    pass

def setopacity(surface, percent):
    s = surface.copy()
    s.fill((255, 255, 255, int(255 * percent / 100)), special_flags=pygame.BLEND_RGBA_MULT)
    return s

def loadimage(path: str):
    full_path = os.path.join(*path.split("/"))
    img = pygame.image.load(full_path)
    return img.convert_alpha() if img.get_alpha() is not None else img.convert()

def loadNthanimation(spritesheet, dimensions: tuple, rowcol: tuple):
    x, y = dimensions
    col, row = rowcol

    sprite_rect = pygame.Rect(col * x, row * y, x, y)
    return spritesheet.subsurface(sprite_rect)

def run(setup=setupgame, update=updategame, draw=drawgame) -> None:
    global dt
    internalsetupgame(setup)
    while running:
        didQuit()
        internalupdategame(update)
        internaldrawgame(draw)
        dt = clock.tick(60) / 1000
        pygame.display.flip()
    pygame.quit()

def keyPressed(key: str) -> bool:
    k = KEY_MAP.get(key)
    if k is None:
        return False
    return pygame.key.get_pressed()[k]