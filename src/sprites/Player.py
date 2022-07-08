import pygame as pg, os
from pygame import Vector2 as vec
pg.init()

WIDTH = 1306
HEIGHT = 526 

def makeAnimation(directory):
    list1 = os.listdir(directory)
    n = len(list1)
    tempList = []
    for i in range(1,n+1):
        if (os.path.exists(f'{directory}{i}.png')):
            tmp = pg.image.load(f'{directory}{i}.png')
            tmp.set_colorkey(0,0,0)
            tempList.append(tmp)
    
    return tempList

def makeAnimationFlip(directory):
    list1 = os.listdir(directory)
    n = len(list1)
    tempList = []
    for i in range(1,n+1):
        if (os.path.exists(f'{directory}{i}.png')):
            tmp = pg.image.load(f'{directory}{i}.png')
            tmp.set_colorkey(0,0,0)
            tempList.append(pg.transform.flip(tmp,True,False))
    
    return tempList

class Player(pg.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.hp = 100
        self.isShooting = False
        self.isDead = False
        self.isJumping = False
        self.isIdle = True
        self.isFlipped = False
        self.shootingCoolDown = 0
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.walkLeft = makeAnimation('resources/images/sprites/heroine/walk/')
        self.walkRight = makeAnimationFlip('resources/images/sprites/heroine/walk/')
        self.idleLeft = makeAnimation('resources/images/sprites/heroine/idle/')
        self.idleRight = makeAnimationFlip('resources/images/sprites/heroine/idle/')
        self.shootLeft = makeAnimation('resources/images/sprites/heroine/shoot/')
        self.shootRight = makeAnimationFlip('resources/images/sprites/heroine/shoot/')
        self.dieLeft = makeAnimation('resources/images/sprites/heroine/die/')
        self.dieRight = makeAnimationFlip('resources/images/sprites/heroine/die/')

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
