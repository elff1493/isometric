import pygame
from game_engine import Window
from game_engine.nodes import Sprite, Node, Tile
from math import atan2, pi, sin, cos

class Isometric(Node):
    image_map = pygame.image.load("iso-64x64-building.png")
    def __init__(self, **k):
        Node.__init__(self, **k)
        self.tile_size = (32, 16)
        self.grid = [[Tile(x, y, parent=self, _id=8) for x in range(50)] for y in range(50)]
        self.pan = (0, 0)
        self.cen = (24, 8)

    def update(self):
        for x, l in enumerate(self.grid):
            for y, tile in enumerate(l):
                tile.x, tile.y = self.to_screen(x - self.pan[0], y - self.pan[1])

    def to_screen(self, x, y):
        x -= self.cen[0]
        y -= self.cen[1]
        return (x - y) * -32, (x + y) * -16

class Player(Sprite):
    def __init__(self, **k):
        Sprite.__init__(self, **k)
        self.sheet = pygame.image.load("skeleton_0.png")
        self.stand = [[self.sheet.subsurface((128*x, 128*y, 128, 128))for y in range(8)] for x in range(5, 9)]
        self.image = self.stand[0][0]
        self.direction = 0

    def look(self, a):
        self.image = self.stand[0][a]

class Game(Window):
    def __init__(self):
        Window.__init__(self, size=(1000, 1000))
        self.grid = Isometric(parent=self)
        self.xy = pygame.Vector2((0, 0))
        self.bg = (100, 100, 100)
        self.player = Player(parent=self, pos=self.size/2, z=1, anchor=(0.5, 0.5))
        self.direction = 0
        self.line = pygame.Vector2(0, 0)

    def event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            on = self.grid.grid[int(self.xy.x)][int(self.xy.y)]
            if e.button == 1:
                on.set_z(on.zi + 1)
            if e.button == 3:
                on.set_z(on.zi - 1)
            if e.button == 4:
                on.id = min(on.id + 1, 80)
            elif e.button == 5:
                on.id = max(on.id - 1, 0)
        if e.type == pygame.MOUSEMOTION:
            a = ((self.size/-2) + e.pos).as_polar()[1]
            self.player.look(int(((a+202.5) / 45)) % 8)
            #a *= pi * 2 / 360
            #self.line = (self.size/-2) + e.pos
            #print(a)
            #a = -atan2(-a.y, a.x)
            self.direction = (a + 150) % 360
            #self.player.look(round(a/45)%7)

    def update(self):
        keys = pygame.key.get_pressed()
        #self.line.x = cos(self.direction) * 100
        #self.line.y = sin(self.direction) * 100
        if keys[pygame.K_a]:
            self.xy.y += sin(self.direction)
            self.xy.x += cos(self.direction)


        if keys[pygame.K_w]:
            self.xy.y += sin(pi*self.direction/180)/5
            self.xy.x += cos(pi*self.direction/180)/5

        self.grid.pan = self.xy
        x = (self.xy[0] / 32 + self.xy[1] / 16) / 2
        y = (self.xy[1] / 16 - (self.xy[0] / 32)) / 2
        x1 = (x - y) * 32
        y1 = (x + y) * 16

        pygame.draw.circle(self.window.screen, (255, 255, 0), (int(x1), int(y1)), 10)
        #self.player.x = pygame.mouse.get_pos()[0]
        #self.player.y = pygame.mouse.get_pos()[1]

    def draw(self):
        pass
        """
        c = ((255, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0),
             (255, 255, 0), (0, 0, 0), (255, 0, 255), (0, 255, 255))
        for i in range(0, 360, 2):
            n = int(((i+202.5) / 45)) % 8
            v = pygame.Vector2(sin(2*pi*i/360)* 100, cos(2*pi*i/360) * 100)
            #print(i, n)
            pygame.draw.line(self.screen, c[n], self.size/2, (self.size/2)+v)
        #pygame.draw.circle(self.window.screen, (255, 255, 255), (250, 250), 10)
        #input()
        """
class Wold:
    def __init__(self):
        self.__chunks = {}
        self.pos = pygame.Vector2()
from struct import pack, unpack

class Chunk:
    def __init__(self, root, b):
        self.xy = pygame.Vector2()
        self.tiles = None
        self.root = root


    def from_bytes(self, b):
        """takes a byte array of 100 byte and two ints at the start"""
        x, y, b = unpack("ii100b", b)
        self.xy.x = x
        self.xy.y = y
        l = []
        for y in range(10):
            l.append(tuple([Tile(x, y, dict(zip(("id", "hitbox", "up"),  # is a mess ill clean up
                unpack("BBb", data[x+y*10:(x+y*10)+3]))))
              for x, data in enumerate(b[y:y+3])]))
        self.tiles = tuple(l)

        for x in range(10):
            for y in range(10):
                a = unpack("BBb", b[x+y*10:(x+y*10)+3])


if __name__ == "__main__":
    g = Game()
    g.mainloop()