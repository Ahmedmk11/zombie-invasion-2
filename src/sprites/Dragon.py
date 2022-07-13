import pygame as pg
import os, InGame
from sprites import Fireball as fb
pg.init()

def makeAnimation(directory):
    list1 = os.listdir(directory)
    n = len(list1)
    tempList = []
    for i in range(1,n+1):
        if (os.path.exists(f'{directory}{i}.png')):
            tmp = pg.image.load(f'{directory}{i}.png')
            # tmp.set_colorkey((0,0,0))
            tempList.append(tmp)
    
    return tempList

def makeAnimationFlip(directory):
    list1 = os.listdir(directory)
    n = len(list1)
    tempList = []
    for i in range(1,n+1):
        if (os.path.exists(f'{directory}{i}.png')):
            tmp = pg.image.load(f'{directory}{i}.png')
            # tmp.set_colorkey((0,0,0))
            tempList.append(pg.transform.flip(tmp,True,False))
    
    return tempList
class Dragon(pg.sprite.Sprite):
    def __init__(self,xpos, ypos, isFlipped, color):
        super().__init__()
        self.speed = 1
        self.updateTime = pg.time.get_ticks()
        self.frameIndex = 0
        self.attackCoolDown = 0
        self.isFlipped = isFlipped
        self.flying = True
        self.isDying = True
        self.hp = 10
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.fireball = ""

        if not self.isFlipped:
            self.action = 0
        elif self.isFlipped:
            self.action = 1

        self.idleLeft = makeAnimation(f'resources/images/sprites/dragons/idle_{self.color}/')
        self.idleRight = makeAnimationFlip(f'resources/images/sprites/dragons/idle_{self.color}/')
        self.dieLeft = makeAnimation(f'resources/images/sprites/dragons/die_{self.color}/')
        self.dieRight = makeAnimationFlip(f'resources/images/sprites/dragons/die_{self.color}/')

        self.anime = []

        self.anime.append(self.idleLeft)
        self.anime.append(self.idleRight)
        self.anime.append(self.dieLeft)
        self.anime.append(self.dieRight)
        
        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)
        
        
    def move(self):
        if not self.hp == 0:
            if not self.isFlipped:
                self.update_action(0)
            elif self.isFlipped:
                self.update_action(1)

        if not self.isFlipped and self.rect.centerx > 1116:
            self.rect.centerx -= self.speed
        if self.isFlipped and self.rect.centerx < 200:
            self.rect.centerx += self.speed

    def attack(self):
        if self.rect.left < 1316 and self.rect.right > 0:
            if not self.isFlipped:
                head = self.rect.left
            else:
                head = self.rect.right

            fireball = fb.Fireball(head, self.rect.centery, self.color)
            InGame.fireball_group.add(fireball)
            return fireball
        return ""

    def update(self):
        if self.flying:
            animation_cooldown = 110
        else:
            animation_cooldown = 60

        if self.attackCoolDown == 0 and InGame.alive:
            # Fireball_sound = mixer.Sound('Fireball.wav')
            # Fireball_sound.play()
            self.fireball = self.attack()

            if self.color == "red":
                self.attackCoolDown = 200
            elif self.color == "yellow":
                self.attackCoolDown = 200


        self.image = self.anime[self.action][self.frameIndex]

        if (self.fireball != "" and self.fireball.flag and abs(self.fireball.rect.centerx - InGame.player.rect.centerx) <= 24
        and abs(self.fireball.rect.centery - InGame.player.rect.centery) <= 32):

            self.fireball.kill()
            if self.color == "yellow":
                InGame.player.getDamage(5)
            else:
                InGame.player.getDamage(5)
            self.fireball.flag = False

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()

            if self.frameIndex == len(self.anime[self.action]) - 1 and self.hp == 0 and self.isDying:
                self.isDying = False
                self.kill()
            else:
                self.frameIndex += 1

        if self.frameIndex >= len(self.anime[self.action]):
            self.frameIndex = 0

        if InGame.alive:
            self.move()

        if self.hp <= 0:
            self.flying = False

        if self.attackCoolDown > 0:
            self.attackCoolDown -= 1

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()