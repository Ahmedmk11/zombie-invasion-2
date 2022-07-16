import math
import pygame as pg, InGame
from pygame import Vector2 as vector
pg.init()
class Fireball(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.speed = 15
        self.color = color
        self.tmp = pg.image.load(f'resources/images/sprites/dragons/fireball_{self.color}.png')
        self.flag = True

        vec = vector(x,y) - vector(InGame.player.rect.centerx, InGame.player.rect.centery)
        unitVec = vector.normalize(vec)
        length = vec.length()
        if y <= length:
            angle = math.acos(y/length)
            if abs(InGame.player.rect.centerx - x) <= 100:
                self.image = pg.transform.rotate(self.tmp, 0)
            elif InGame.player.rect.centerx - x > 0:
                self.image = pg.transform.rotate(self.tmp, angle / (math.pi/180))
            elif InGame.player.rect.centerx - x < 0:
                self.image = pg.transform.rotate(self.tmp, -angle / (math.pi/180))
        else:
            self.image = self.tmp

        self.velVec = unitVec * self.speed
        self.rect = self.image.get_rect(center = (x,y))
        
        InGame.fireballSFX.play()
        
    def update(self):
        self.rect.center -= self.velVec
        if self.rect.left >= 1321 or self.rect.right <= -5 or self.rect.bottom > 620:  
            self.kill()
        InGame.screen.blit(self.image,self.rect)
        