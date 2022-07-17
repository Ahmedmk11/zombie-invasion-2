"""Dragon

Contains the class Dragon

"""

import in_game
import os

import pygame as pg

from sprites import fireball
from typing import Union

pg.init()


def make_animation(directory: str) -> list[pg.Surface]:
    """

    :param directory: takes in the directory of the files of the animations
    :return: a list containing all animation frames
    """

    list1 = os.listdir(directory)
    n = len(list1)
    temp_list = []
    for i in range(1, n + 1):
        if os.path.exists(f'{directory}{i}.png'):
            tmp = pg.image.load(f'{directory}{i}.png')
            temp_list.append(tmp)

    return temp_list


def make_animation_flip(directory: str) -> list[pg.Surface]:
    """

    :param directory: takes in the directory of the files of the animations
    :return: a list containing all animation frames but flipped to face right
    """

    list1 = os.listdir(directory)
    n = len(list1)
    temp_list = []
    for i in range(1, n + 1):
        if os.path.exists(f'{directory}{i}.png'):
            tmp = pg.image.load(f'{directory}{i}.png')
            temp_list.append(pg.transform.flip(tmp, True, False))

    return temp_list


class Dragon(pg.sprite.Sprite):
    """

    A class used to represent a Dragon object
    This class defines the following methods:
        * move
        * attack
        * update
        * update_action
    """

    def __init__(self, xpos: int, ypos: int, is_flipped: bool, color: str) -> None:
        super().__init__()
        self.speed = 1
        self.updateTime = pg.time.get_ticks()
        self.frameIndex = 0
        self.attackCoolDown = 0
        self.isFlipped = is_flipped
        self.flying = True
        self.isDying = True
        self.hp = 10
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.fireball = ""

        if not self.isFlipped:
            self.action = 0
        elif self.isFlipped:
            self.action = 1

        self.idleLeft = make_animation(f'resources/images/sprites/dragons/idle_{self.color}/')
        self.idleRight = make_animation_flip(f'resources/images/sprites/dragons/idle_{self.color}/')
        self.dieLeft = make_animation(f'resources/images/sprites/dragons/die_{self.color}/')
        self.dieRight = make_animation_flip(f'resources/images/sprites/dragons/die_{self.color}/')

        self.anime = []

        self.anime.append(self.idleLeft)
        self.anime.append(self.idleRight)
        self.anime.append(self.dieLeft)
        self.anime.append(self.dieRight)

        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)

    def move(self) -> None:
        """

        This function is responsible for moving the dragon and triggering the animation
        """

        if not self.hp == 0:
            if not self.isFlipped:
                self.update_action(0)
            elif self.isFlipped:
                self.update_action(1)

        if not self.isFlipped and self.rect.centerx > 1116:
            self.rect.centerx -= self.speed
        if self.isFlipped and self.rect.centerx < 200:
            self.rect.centerx += self.speed

    def attack(self) -> Union[fireball.Fireball, str]:
        """

        :return: a new fireball object everytime attack is called
        """

        if self.rect.left < 1316 and self.rect.right > 0:
            if not self.isFlipped:
                head = self.rect.left
            else:
                head = self.rect.right

            self.fireball = fireball.Fireball(head, self.rect.centery, self.color)
            in_game.fireball_group.add(self.fireball)
            return self.fireball
        return ""

    def update(self) -> None:
        """

        This function updates the dragon object every frame during the game
        """

        if self.flying:
            animation_cooldown = 110
        else:
            animation_cooldown = 20

        if self.attackCoolDown == 0 and in_game.alive:
            self.fireball = self.attack()

            if self.color == "red":
                self.attackCoolDown = 200
            elif self.color == "yellow":
                self.attackCoolDown = 300

        self.image = self.anime[self.action][self.frameIndex]

        if (self.fireball != "" and self.fireball.flag and abs(
                self.fireball.rect.centerx - in_game.player_obj.rect.centerx) <= 24
                and abs(self.fireball.rect.centery - in_game.player_obj.rect.centery) <= 32):

            self.fireball.kill()
            if self.color == "yellow":
                in_game.player_obj.get_damage(15)
                in_game.hitSFX.play()
            else:
                in_game.player_obj.get_damage(25)
                in_game.hitSFX.play()
            self.fireball.flag = False

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()

            if self.frameIndex == len(self.anime[self.action]) - 1 and self.hp == 0 and self.isDying:
                self.isDying = False
                self.kill()
            else:
                self.frameIndex += 1

        if self.frameIndex >= len(self.anime[self.action]):
            self.frameIndex = 0

        if in_game.alive:
            self.move()

        if self.hp <= 0:
            self.flying = False

        if self.attackCoolDown > 0:
            self.attackCoolDown -= 1

    def update_action(self, new_action: int) -> None:
        """

        :param new_action: a new action to replace the old one
        """

        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()
