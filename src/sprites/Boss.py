import os
import pygame as pg
from sprites import Zombie as zm
import InGame

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

class Boss(zm.Zombie): 
    def __init__(self):
        zm.Zombie.__init__(self,3,True)
        self.isFlipped = False
        self.hp = 3000
        self.walkLeft = makeAnimation('resources/images/sprites/boss/walk/')
        self.walkRight = makeAnimationFlip('resources/images/sprites/boss/walk/')
        self.idleLeft = makeAnimation('resources/images/sprites/boss/idle/')
        self.idleRight = makeAnimationFlip('resources/images/sprites/boss/idle/')
        self.attackLeft = makeAnimation('resources/images/sprites/boss/attack/')
        self.attackRight = makeAnimationFlip('resources/images/sprites/boss/attack/')
        self.appearLeft = makeAnimation('resources/images/sprites/boss/appear/')
        self.appearRight = makeAnimationFlip('resources/images/sprites/boss/appear/')
        self.dieLeft = makeAnimation('resources/images/sprites/boss/die/')
        self.dieRight = makeAnimationFlip('resources/images/sprites/boss/die/')
        self.anime = []
        self.anime.append(self.idleLeft)
        self.anime.append(self.idleRight)
        self.anime.append(self.walkLeft)
        self.anime.append(self.walkRight)
        self.anime.append(self.attackLeft)
        self.anime.append(self.attackRight)
        self.anime.append(self.appearLeft)
        self.anime.append(self.appearRight)
        self.anime.append(self.dieLeft)
        self.anime.append(self.dieRight)

        self.action = 6

        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (877,610)

    def checkAttackRange(self):
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 35) and (not self.isFlipped and self.rect.centerx >= InGame.player.rect.centerx):
            return True
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 300) and (self.isFlipped and self.rect.centerx <= InGame.player.rect.centerx):
            return True
        return False

    def getDamage(self, val):
        self.hp -= val