import pygame as pg
from pygame import Vector2 as vec
pg.init()

WIDTH = 1306
HEIGHT = 526 

class Player(pg.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.spriteSheet = pg.image.load(filename).convert()
        self.hp = 100
        self.isShoot = False
        self.isDead = False
        self.isJump = False
        self.isIdle = True
        self.coolDown = 0
        self.pos = vec(WIDTH/2,HEIGHT/2)

    def getSprite(self, x, y, w, h):
        sprite = pg.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.spriteSheet,(0,0),(x,y,w,h))
        return sprite

    def move():
        pass

    def jump():
        pass

    def idle():
        pass

    def shoot():
        pass

    def getDamage():
        pass

    def die():
        pass

    def draw():
        pass

    def update():
        pass
