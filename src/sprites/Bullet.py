from random import randrange
import pygame as pg, os, InGame
from pygame import Vector2 as vec
from sprites import Player as pl
pg.init()

WIDTH = 1316
HEIGHT = 526
ACCELERATION = 0.7
FRICTION = -0.12
GRAVITY = 9.8

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__()
        self.direction = direction
        self.speed = 10
        self.index = randrange(1,2)
        self.tmp = pg.image.load(f'resources/images/sprites/heroine/{self.index}.png')
        if self.direction == 1:
            self.image = self.tmp
        if self.direction == -1:
            self.image = pg.transform.flip(self.tmp)
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.x -= (self.direction * self.speed)

        if self.rect.left >= WIDTH+5 or self.rect.right <= -5:  
            self.kill()
        InGame.screen.blit(self.image,self.rect)