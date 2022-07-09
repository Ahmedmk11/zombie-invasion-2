import pygame as pg, os, InGame
from pygame import Vector2 as vec
pg.init()

WIDTH = 1316
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
        self.frameIndex = 0
        self.action = 0
        self.hp = 100
        self.vel_vec = vec(0,0)
        self.acc_vec = vec(0,0)
        self.isShooting = False
        self.isDead = False
        self.isJumping = False
        self.isIdle = True
        self.isFlipped = False
        self.shootingCoolDown = 0

        self.walkLeft = makeAnimation('resources/images/sprites/heroine/walk/')
        self.walkRight = makeAnimationFlip('resources/images/sprites/heroine/walk/')
        self.idleLeft = makeAnimation('resources/images/sprites/heroine/idle/')
        self.idleRight = makeAnimationFlip('resources/images/sprites/heroine/idle/')
        self.shootLeft = makeAnimation('resources/images/sprites/heroine/shoot/')
        self.shootRight = makeAnimationFlip('resources/images/sprites/heroine/shoot/')
        self.dieLeft = makeAnimation('resources/images/sprites/heroine/die/')
        self.dieRight = makeAnimationFlip('resources/images/sprites/heroine/die/')
        self.anime = []
        self.anime.append(self.idleLeft)
        self.anime.append(self.idleRight)
        self.anime.append(self.walkLeft)
        self.anime.append(self.walkRight)
        self.anime.append(self.shootLeft)
        self.anime.append(self.shootRight)
        self.anime.append(self.dieLeft)
        self.anime.append(self.dieRight)

        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.rect.midbottom = self.pos
        

    def move(self, movingLeft, movingRight):
        self.acc_vec = vec(0,ACCELERATION)
        if movingLeft:
            self.acc_vec.x = -ACCELERATION
            self.isFlipped = False

        if movingRight:
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


    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(InGame.player_group.sprite, InGame.platform_group,False)
        self.rect.y -= -1
        if hits:
            # jump_sound = mixer.Sound('Jump.wav')
            # jump_sound.play()
            self.vel_vec.y = -15

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
        self.image = self.anime[self.action][self.frameIndex]

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()
            self.frameIndex += 1

        if self.frameIndex >= len(self.anime[self.action]):
            self.frameIndex = 0

        if self.shootingCoolDown > 0:
            self.shootingCoolDown -= 1

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.updateTime = pg.time.get_ticks()