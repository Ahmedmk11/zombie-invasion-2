"""Fireball

Contains the class Fireball

"""

import math

import in_game
import pygame as pg
from pygame import Vector2

pg.init()


class Fireball(pg.sprite.Sprite):
    """

    A class used to represent the fireball objects for dragons
    """

    def __init__(self, x: int, y: int, color: str) -> None:
        super().__init__()
        self.speed = 15
        self.color = color
        self.tmp = pg.image.load(f'resources/images/sprites/dragons/fireball_{self.color}.png')
        self.flag = True

        vec = Vector2(x, y) - Vector2(in_game.player_obj.rect.centerx, in_game.player_obj.rect.centery)
        unit_vec = Vector2.normalize(vec)
        length = vec.length()
        if y <= length:
            angle = math.acos(y / length)
            if abs(in_game.player_obj.rect.centerx - x) <= 100:
                self.image = pg.transform.rotate(self.tmp, 0)
            elif in_game.player_obj.rect.centerx - x > 0:
                self.image = pg.transform.rotate(self.tmp, angle / (math.pi / 180))
            elif in_game.player_obj.rect.centerx - x < 0:
                self.image = pg.transform.rotate(self.tmp, -angle / (math.pi / 180))
        else:
            self.image = self.tmp

        self.velVec = unit_vec * self.speed
        self.rect = self.image.get_rect(center=(x, y))

        in_game.fireballSFX.play()

    def update(self) -> None:
        """

        This function updates the fireball object every frame during the game
        """

        self.rect.center -= self.velVec
        if self.rect.left >= 1321 or self.rect.right <= -5 or self.rect.bottom > 620:
            self.kill()
        in_game.screen.blit(self.image, self.rect)
