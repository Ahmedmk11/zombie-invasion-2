import pygame as pg, os, InGame
from pygame import Vector2 as vec
pg.init()

WIDTH = 1306
HEIGHT = 526 
ACCELERATION = 0.7
FRICTION = -0.12
GRAVITY = 9.8

def makeAnimation(directory):
    list1 = os.listdir(directory)
    n = len(list1)
    tempList = []
    for i in range(1,n+1):
        if (os.path.exists(f'{directory}{i}.png')):
            tmp = pg.image.load(f'{directory}{i}.png')
            tmp.set_colorkey((0,0,0))
            tempList.append(tmp)
    
    return tempList

def makeAnimationFlip(directory):
    list1 = os.listdir(directory)
    n = len(list1)
    tempList = []
    for i in range(1,n+1):
        if (os.path.exists(f'{directory}{i}.png')):
            tmp = pg.image.load(f'{directory}{i}.png')
            tmp.set_colorkey((0,0,0))
            tempList.append(pg.transform.flip(tmp,True,False))
    
    return tempList

class Player(pg.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.updateTime = pg.time.get_ticks()
        self.frame_index = 0
        self.hp = 100
        self.vel_vec = vec(0,0)
        self.acc_vec = vec(0,0)
        self.isShooting = False
        self.isDead = False
        self.isJumping = False
        self.isIdle = True
        self.isFlipped = False
        self.movingLeft = False
        self.movingRight = False
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
        self.image = self.idleLeft[self.frame_index]
        self.rect = self.image.get_rect()

    def move(self):
        if self.movingLeft:
            self.acc_vec.x = -ACCELERATION
            self.isFlipped = False

        elif self.movingRight:
            self.acc_vec.x = ACCELERATION
            self.isFlipped = True

        self.acc_vec.x += self.vel_vec.x * FRICTION
        self.vel_vec += self.acc_vec
        self.pos += self.vel_vec + 0.5 * self.acc_vec
        self.rect.midbottom = self.pos

        hits = pg.sprite.spritecollide(InGame.player_group.sprite, InGame.platform_group,False)
        if hits:
            self.pos.y = hits[0].rect.top
            self.vel_vec.y = 0


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

    def draw(self):
        self.screen.blit(self.image,self.rect)

    def update(self):

        animation_cooldown = 75

        if self.movingLeft:
            self.image = self.movingLeft[self.frame_index]
        elif self.movingRight:
            self.image = self.movingRight[self.frame_index]

        elif not self.movingLeft and not self.movingRight and not self.isShooting and not self.isDead:
            self.isIdle = True
            if self.isFlipped:
                self.image = self.idleRight[self.frame_index]
            elif not self.isFlipped:
                self.image = self.idleLeft[self.frame_index]

        elif self.isShooting:
            if self.isFlipped:
                self.image = self.shootRight[self.frame_index]
            elif not self.isFlipped:
                self.image = self.shootLeft[self.frame_index]

        elif self.isDead:
            if self.isFlipped:
                self.image = self.dieRight[self.frame_index]
            elif not self.isFlipped:
                self.image = self.dieLeft[self.frame_index]

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()
            self.frame_index += 1
        
        if self.movingLeft and self.frame_index >= len(self.movingLeft):
            self.frame_index = 0
        elif self.movingRight and self.frame_index >= len(self.movingRight):
            self.frame_index = 0

        elif self.isIdle:

            if self.isFlipped and self.frame_index >= len(self.idleRight):
                self.frame_index = 0
            elif not self.isFlipped and self.frame_index >= len(self.idleLeft):
                self.frame_index = 0

        elif self.isShooting:
   
            if self.isFlipped and self.frame_index >= len(self.shootRight):
                self.frame_index = 0
            elif not self.isFlipped and self.frame_index >= len(self.shootLeft):
                self.frame_index = 0

        elif self.isDead:

            if self.isFlipped and self.frame_index >= len(self.dieRight):
                self.frame_index = 0
            elif not self.isFlipped and self.frame_index >= len(self.dieLeft):
                self.frame_index = 0

        if self.shootingCoolDown > 0:
            self.shootingCoolDown -= 1
