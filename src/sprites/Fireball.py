import math
import pygame as pg, InGame
from pygame import Vector2 as vector
pg.init()
class Fireball(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.speed = 10
        self.color = color
        self.tmp = pg.image.load(f'resources/images/sprites/dragons/fireball_{self.color}.png')

        vec = vector(x,y) - vector(InGame.player.rect.centerx, InGame.player.rect.centery)
        unitVec = vector.normalize(vec)
        length = vec.length()
        if y <= length:
            angle = math.acos(y/length)
            self.image = pg.transform.rotate(self.tmp, 2 * angle)
        else:
            self.image = self.tmp

        self.velVec = unitVec * self.speed
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.center -= self.velVec
        if self.rect.left >= 1321 or self.rect.right <= -5 or self.rect.bottom > 570:  
            self.kill()
        InGame.screen.blit(self.image,self.rect)