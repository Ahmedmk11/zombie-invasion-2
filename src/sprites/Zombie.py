import pygame as pg
from PIL import Image
import os, InGame
pg.init()

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

class Zombie(pg.sprite.Sprite):
    def __init__(self,xpos,speed,isFlipped, isBoss):
        super().__init__()
        self.speed = speed
        self.updateTime = pg.time.get_ticks()
        self.frameIndex = 0
        self.attackCoolDown = 0
        self.isFlipped = isFlipped
        self.appearing = True
        self.walking = False
        self.attacking = False
        self.isDying = True
        self.isBoss = isBoss

        if not self.isFlipped:
            self.action = 6
        elif self.isFlipped:
            self.action = 7

        if not self.isBoss:
            self.hp = 10
            self.walkLeft = makeAnimation('resources/images/sprites/zombies/walk/')
            self.walkRight = makeAnimationFlip('resources/images/sprites/zombies/walk/')
            self.idleLeft = makeAnimation('resources/images/sprites/zombies/idle/')
            self.idleRight = makeAnimationFlip('resources/images/sprites/zombies/idle/')
            self.attackLeft = makeAnimation('resources/images/sprites/zombies/attack/')
            self.attackRight = makeAnimationFlip('resources/images/sprites/zombies/attack/')
            self.appearLeft = makeAnimation('resources/images/sprites/zombies/appear/')
            self.appearRight = makeAnimationFlip('resources/images/sprites/zombies/appear/')
            self.dieLeft = makeAnimation('resources/images/sprites/zombies/die/')
            self.dieRight = makeAnimationFlip('resources/images/sprites/zombies/die/')
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
        else:
            self.hp = 2000
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
        
        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        if not isBoss:
            self.rect.midbottom = (xpos,555)
        else:
            self.rect.midbottom = (xpos,550)

        
    def move(self):

        if self.walking and not self.hp == 0:
            if not self.isFlipped:
                self.update_action(2)
            elif self.isFlipped:
                self.update_action(3)

        if not self.isFlipped:
            self.rect.centerx -= self.speed
        if self.isFlipped:
            self.rect.centerx += self.speed

    def attack(self):
        if self.attacking and not self.hp == 0:
            if not self.isFlipped:
                self.update_action(4)
            if self.isFlipped:
                self.update_action(5)

    def checkAttackRange(self):
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 35) and (not self.isFlipped and self.rect.centerx > InGame.player.rect.centerx):
            return True
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 70) and (self.isFlipped and self.rect.centerx < InGame.player.rect.centerx):
            return True
        return False

    def checkDamageRange(self):
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 35):
            return True
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 65):
            return True
        return False

    def update(self):
        if self.attacking:
            animation_cooldown = 125
        elif self.appearing and not self.isBoss:
            animation_cooldown = 100
        elif self.appearing and self.isBoss:
            animation_cooldown = 120
        elif self.hp == 0:
            animation_cooldown = 60
        else:
            animation_cooldown = 90

        self.image = self.anime[self.action][self.frameIndex]

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()
            
            if self.appearing and self.frameIndex == len(self.anime[self.action]) - 1:
                self.appearing = False
                self.walking = True
            else:
                self.frameIndex += 1

            if self.frameIndex == len(self.anime[self.action]) - 1 and self.hp == 0 and self.isDying:
                self.isDying = False
                self.kill()
            else:
                self.frameIndex += 1

            if self.attacking and self.frameIndex == len(self.anime[self.action]) - 1:
                InGame.player.getDamage(10)
            if pg.sprite.spritecollide(InGame.player_group.sprite,InGame.zombies_group,False) and self.checkDamageRange():
                InGame.player_group.sprite.getDamage(0.5)

        if self.frameIndex >= len(self.anime[self.action]):
            self.frameIndex = 0

        if InGame.alive and not self.attacking:
            self.move()
        if not self.appearing:
            if self.checkAttackRange():
                self.attacking = True
                self.walking = False
                self.attack()
            else:
                self.attacking = False
                self.walking = True


        if self.attackCoolDown > 0:
            self.attackCoolDown -= 1

        if self.rect.centerx >= 1336 or self.rect.centerx <= -20:
            self.kill()

        if not self.isFlipped and not InGame.alive:
            self.update_action(0)
        if self.isFlipped and not InGame.alive:
            self.update_action(1)

        if self.isBoss:
            pass

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()