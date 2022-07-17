"""Platform

Contains the class Platform

"""

import pygame as pg

pg.init()


class Platform(pg.sprite.Sprite):
    """

    This class is used to create a platform object to be used as the game floor
    """

    def __init__(self) -> None:
        super().__init__()
        self.image = pg.Surface((1316, 185))
        self.image.fill((105, 105, 105))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 610
