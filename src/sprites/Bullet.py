from random import randrange
import pygame as pg, InGame
pg.init()
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__()
        self.direction = direction
        self.speed = 20
        self.index = randrange(1,2)
        self.tmp = pg.image.load(f'resources/images/sprites/heroine/{self.index}.png')
        if self.direction == 1:
            self.image = self.tmp
        if self.direction == -1:
            self.image = pg.transform.flip(self.tmp, True, False)
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.x -= (self.direction * self.speed)
        if self.rect.left >= 1321 or self.rect.right <= -5:  
            self.kill()
        InGame.screen.blit(self.image,self.rect)