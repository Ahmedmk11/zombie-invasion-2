import pygame as pg, os, InGame
from sprites import Bullet as bt
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
    def __init__(self):
        super().__init__()
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
        self.direction = 1

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
        
        

    def move(self):
        self.acc_vec = vec(0,ACCELERATION)
        if InGame.isMovingLeft:
            self.acc_vec.x = -ACCELERATION
            self.isFlipped = False
            self.direction = 1

        if InGame.isMovingRight:
            self.acc_vec.x = ACCELERATION
            self.isFlipped = True
            self.direction = -1

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

    def shoot(self):
        bullet = bt.Bullet(self.rect.centerx - (0.5 * self.direction * self.rect.size[0]), self.rect.centery - 7, self.direction)
        InGame.bullet_group.add(bullet)

    def getDamage(self, val):
        self.health -= val
        # hit_sound = mixer.Sound('Hit.wav')
        # hit_sound.play()

    def die(self):
        InGame.alive = False
        if not InGame.zombie.isFlipped:
            InGame.isIdleLeftZombie = True
        else:
            InGame.isIdleRightZombie = True
        if not self.isFlipped:
            InGame.isMovingLeft = False
            InGame.isMovingRight = False
            InGame.isIdleLeft = False
            InGame.isIdleRight = False
            InGame.isShootingLeft = False
            InGame.isShootingRight = False
            InGame.isDeadLeft = True
        if self.isFlipped:
            InGame.isMovingLeft = False
            InGame.isMovingRight = False
            InGame.isIdleLeft = False
            InGame.isIdleRight = False
            InGame.isShootingLeft = False
            InGame.isShootingRight = False
            InGame.isDeadRight = True

    def draw(self):
        InGame.screen.blit(self.image,self.rect)

    def update(self):
        animation_cooldown = 75
        self.image = self.anime[self.action][self.frameIndex]

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()
            if not InGame.alive and self.frameIndex == len(self.anime[self.action]) - 1:
                self.frameIndex == len(self.anime[self.action]) - 1
            else:
                self.frameIndex += 1

        if self.frameIndex >= len(self.anime[self.action]) and InGame.alive:
            self.frameIndex = 0

        if self.shootingCoolDown > 0:
            self.shootingCoolDown -= 1

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()