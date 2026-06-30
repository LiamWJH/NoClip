import pygame
import math, os


screen = None
clock = None
dt = 0
running = True

class Assets:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
    def image(self, *names, fileformat="png"):
        buffer = []
        for name in names:
            if name not in self.images:
                img = pygame.image.load(f"assets/{name}.{fileformat}")
                self.images[name] = (img.convert_alpha() if img.get_alpha() is not None else img.convert())
            buffer.append(self.images[name])
        return buffer[0] if len(buffer) == 1 else buffer
    def sound(self, *names, fileformat="wav", volume=None):
        buffer = []

        for name in names:
            if name not in self.sounds:
                self.sounds[name] = pygame.mixer.Sound(f"assets/{name}.{fileformat}")

            if volume is not None:
                self.sounds[name].set_volume(volume)

            buffer.append(self.sounds[name])

        return buffer[0] if len(buffer) == 1 else buffer
    def music(self, name, fileformat="wav"):
        pygame.mixer.music.load(f"assets/{name}.{fileformat}")
        pygame.mixer.music.play(-1)
    def font(self, *names, fileformat="ttf"):
        buffer = []
        for name in names:
            if name not in self.fonts:
                self.fonts[name] = (pygame.font.Font(f"assets/{name}.{fileformat}", 32))
            buffer.append(self.fonts[name])
        return buffer[0] if len(buffer) == 1 else buffer
assets = Assets()


class Err(Exception):
    def __init__(self, err, msg):
        self.err = err
        self.msg = msg
    def show(self):
        print(f"{self.__class__.__name__} Error: \n'{self.err}': {self.msg}")

class NoExistError(Err): pass

class view:
    def __init__(self, coords, distance):
        self.x, self.y = coords
        self.distance = distance
    def move_view_xy(self, N):
        direction, distance = N
        rad = math.radians(direction)
        self.x += distance * math.sin(rad)
        self.y -= distance * math.cos(rad)
    def move_view_z(self, distance):
        self.distance += distance
camera = view((0,0), 1)

class thing:
    def __init__(self, name, coords, shape):
        self.name = name
        self.x, self.y = coords
        self.shape = shape
        self.width, self.height = self.size()
        self.children = []

        self.update = None
        self.timer = {}

    def spawn(self, model, x, y):
        model.x = x
        model.y = y
        self.newchild(model)


    def add_timer(self, name):
        self.timer[name] = 0

    def do_updates(self):
        self.update()

    def size(self):
        if self.shape is None:
            return (32, 32)
        return self.shape.get_size()

    def setsize(self, w, h):
        self.width, self.height = w, h

    def AABB(self, scaled=False):
        w = self.width * (camera.distance if scaled else 1)
        h = self.height * (camera.distance if scaled else 1)
        return {"x1": self.x, "x2": self.x + w, "y1": self.y, "y2": self.y + h}

    def overlapswith(self, t):
        a = self.AABB(scaled=True)
        b = t.AABB(scaled=True)
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

def space_001_update(self):
    bigthing.x = centerX(space_001.width, bigthing.width)
    bigthing.y = centerY(space_001.height, bigthing.height)
space_001.update = space_001_update

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
    pygame.mixer.init()
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


def do_updates_for_things(t):
    if t.update:
        t.update(t)
    for child in t.children:
        do_updates_for_things(child)

def internalupdategame(logic) -> None:
    do_updates_for_things(space_001)
    logic()

def updategame() -> None:
    pass


def blitthing(t, parent) -> None:
    scaled_w = int(t.width * camera.distance)
    scaled_h = int(t.height * camera.distance)
    abs_x = parent.x + t.x - camera.x - (scaled_w - t.width) / 2
    abs_y = parent.y + t.y - camera.y - (scaled_h - t.height) / 2
    if t.shape is None:
        screen.blit(_, (abs_x, abs_y))
    else:
        scaled = pygame.transform.scale(t.shape, (scaled_w, scaled_h))
        screen.blit(scaled, (abs_x, abs_y))
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
        update_input()
        internalupdategame(update)
        internaldrawgame(draw)
        dt = clock.tick(500) / 1000
        pygame.display.flip()
    pygame.quit()

_keys_now = {}
_keys_prev = {}


def update_input():
    global _keys_now, _keys_prev

    pygame.event.pump()

    _keys_prev = _keys_now.copy()

    pressed = pygame.key.get_pressed()

    _keys_now = {
        name: pressed[keycode]
        for name, keycode in KEY_MAP.items()
    }


def keyPressed(key: str) -> bool:
    return _keys_now.get(key, False)


def keyJustPressed(key: str) -> bool:
    return _keys_now.get(key, False) and not _keys_prev.get(key, False)


def keyJustReleased(key: str) -> bool:
    return not _keys_now.get(key, False) and _keys_prev.get(key, False)