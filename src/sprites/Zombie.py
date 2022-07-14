import random
import pygame as pg
from pygame import Vector2 as vector
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
    def __init__(self,speed, isBoss):
        super().__init__()
        self.speed = speed
        self.updateTime = pg.time.get_ticks()
        self.frameIndex = 0
        self.attackCoolDown = 0
        self.appearing = True
        self.walking = False
        self.attacking = False
        self.isDying = True
        self.isBoss = isBoss
        random_side = random.randrange(0,2)

        if random_side == 0: 
            random_xpos = range(-20,180)
            self.isFlipped = True
        else:
            random_xpos = range(1136,1336)
            self.isFlipped = False

        if not self.isFlipped:
            self.action = 6
        elif self.isFlipped:
            self.action = 7

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
        
        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.choice(random_xpos),555)

        
    def move(self):

        if self.walking and not self.hp <= 0:
            if not self.isFlipped:
                self.update_action(2)
            elif self.isFlipped:
                self.update_action(3)

        if not self.isFlipped:
            self.rect.centerx -= self.speed
        if self.isFlipped:
            self.rect.centerx += self.speed

    def attack(self):
        if self.attacking and not self.hp <= 0:
            if not self.isFlipped:
                self.update_action(4)
            if self.isFlipped:
                self.update_action(5)

    def checkAttackRange(self):
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 35) and (not self.isFlipped and self.rect.centerx >= InGame.player.rect.centerx):
            return True
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 70) and (self.isFlipped and self.rect.centerx <= InGame.player.rect.centerx):
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
            animation_cooldown = 105
        elif self.hp <= 0 and not self.isBoss:
            animation_cooldown = 60
        elif self.hp <= 0 and self.isBoss:
            animation_cooldown = 100
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

            if self.frameIndex == len(self.anime[self.action]) - 1 and self.hp <= 0 and self.isDying:
                self.isDying = False
                self.kill()
            else:
                self.frameIndex += 1

            if self.attacking and self.frameIndex == len(self.anime[self.action]) - 1:
                if not self.isBoss:
                    InGame.player.getDamage(10)
                else:
                    InGame.player.getDamage(50)



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

        if not self.isBoss and (self.rect.centerx >= 1336 or self.rect.centerx <= -20):
            self.kill()
        
        if self.isBoss:

            if InGame.player.rect.left >= self.rect.right:
                rightDist = InGame.player.rect.left - self.rect.right
                leftDist = (InGame.WIDTH - InGame.player.rect.right) + self.rect.left
            else:
                rightDist = InGame.player.rect.left + (InGame.WIDTH - self.rect.right)
                leftDist = self.rect.left - InGame.player.rect.right

            if not self.isFlipped:
                if rightDist <= leftDist:
                    self.isFlipped = True
            else:
                if rightDist > leftDist:
                    self.isFlipped = False

            if self.hp <= 0:
                InGame.alive = False
                if not self.isFlipped:
                    InGame.isMovingLeft = False
                    InGame.isMovingRight = False
                    InGame.isIdleLeft = True
                    InGame.isIdleRight = False
                    InGame.isShootingLeft = False
                    InGame.isShootingRight = False
                    InGame.isDeadLeft = False
                if self.isFlipped:
                    InGame.isMovingLeft = False
                    InGame.isMovingRight = False
                    InGame.isIdleLeft = False
                    InGame.isIdleRight = True
                    InGame.isShootingLeft = False
                    InGame.isShootingRight = False
                    InGame.isDeadRight = False

        if not self.isBoss or (self.isBoss and self.hp > 0):
            if not self.isFlipped and not InGame.alive:
                self.update_action(0)
            if self.isFlipped and not InGame.alive:
                self.update_action(1)

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()