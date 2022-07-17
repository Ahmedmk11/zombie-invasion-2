"""Bullet

Contains the class Bullet

"""

from random import randrange

import in_game
import pygame as pg

pg.init()


class Bullet(pg.sprite.Sprite):
    """

    A class used to represent the bullet objects for the player
    """

    def __init__(self, x: int, y: int, direction: int, angle: bool) -> None:
        super().__init__()
        self.direction = direction
        self.angle = angle
        self.speed = 20
        self.index = randrange(1, 2)
        self.tmp = pg.image.load(f'resources/images/sprites/heroine/{self.index}.png')

        if self.direction == 1:
            self.image = self.tmp
            if in_game.isShootingLeftUp:
                self.image = pg.transform.rotate(self.image, -45)

        if self.direction == -1:
            self.image = pg.transform.flip(self.tmp, True, False)
            if in_game.isShootingRightUp:
                self.image = pg.transform.rotate(self.image, 45)
        self.rect = self.image.get_rect(center=(x, y))

        in_game.bulletSFX.play()

    def update(self) -> None:
        """

        This function updates the bullet object every frame during the game
        """

        self.rect.x -= (self.direction * self.speed)
        if self.angle:
            self.rect.y -= self.speed - 10
        if self.rect.left >= 1321 or self.rect.right <= -5:
            self.kill()
        if in_game.bossExists:
            if in_game.level == 6 and in_game.boss_obj.hp > 0 and ((self.direction == 1 and (
                    self.rect.left >= in_game.boss_obj.rect.left) and (self.rect.left - in_game.boss_obj.rect.centerx) < 45) or (
                                                                           self.direction == -1 and (in_game.boss_obj.rect.right >= self.rect.right)
                                                                           and (in_game.boss_obj.rect.centerx - self.rect.right) < 45)):
                if self.rect.centery > 350:
                    in_game.boss_obj.get_damage(10)
                if 182 < self.rect.centery <= 350 or in_game.boss_obj.attacking:
                    in_game.boss_obj.get_damage(20)
                self.kill()
        in_game.screen.blit(self.image, self.rect)
