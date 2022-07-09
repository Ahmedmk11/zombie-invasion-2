import pygame as pg
pg.init()
class Platform(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((1316,185))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 555