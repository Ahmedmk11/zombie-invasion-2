"""Boss

Contains the class Boss for level 6 in the game story mode

"""

import os
import random
import pygame as pg
from sprites import zombie
from pygame import mixer
import in_game


def make_animation(directory: str) -> list[pg.Surface]:
    """

    :param directory: takes in the directory of the files of the animations
    :return: returns a list containing all animation frames
    """

    list1 = os.listdir(directory)
    n = len(list1)
    temp_list = []
    for i in range(1, n + 1):
        if os.path.exists(f'{directory}{i}.png'):
            tmp = pg.image.load(f'{directory}{i}.png')
            tmp.set_colorkey((0, 0, 0))
            temp_list.append(tmp)

    return temp_list


def make_animation_flip(directory: str) -> list[pg.Surface]:
    """

    :param directory: takes in the directory of the files of the animations
    :return: returns a list containing all animation frames but flipped to face right
    """

    list1 = os.listdir(directory)
    n = len(list1)
    temp_list = []
    for i in range(1, n + 1):
        if os.path.exists(f'{directory}{i}.png'):
            tmp = pg.image.load(f'{directory}{i}.png')
            tmp.set_colorkey((0, 0, 0))
            temp_list.append(pg.transform.flip(tmp, True, False))

    return temp_list


class Boss(zombie.Zombie):
    """

    A class used to represent the zombie boss object for a final fight in level 6
    This class is a child of Zombie and inherits the following methods:
        * move
        * attack
        * check_damage_range
        * update
        * update_action

    It defines this method:
        * get_damage

    And overrides these methods:
        * __init__ constructor
        * check_attack_range
    """

    def __init__(self) -> None:
        zombie.Zombie.__init__(self, 3, True)
        self.isFlipped = False
        self.hp = 3000
        self.walkLeft = make_animation('resources/images/sprites/boss/walk/')
        self.walkRight = make_animation_flip('resources/images/sprites/boss/walk/')
        self.idleLeft = make_animation('resources/images/sprites/boss/idle/')
        self.idleRight = make_animation_flip('resources/images/sprites/boss/idle/')
        self.attackLeft = make_animation('resources/images/sprites/boss/attack/')
        self.attackRight = make_animation_flip('resources/images/sprites/boss/attack/')
        self.appearLeft = make_animation('resources/images/sprites/boss/appear/')
        self.appearRight = make_animation_flip('resources/images/sprites/boss/appear/')
        self.dieLeft = make_animation('resources/images/sprites/boss/die/')
        self.dieRight = make_animation_flip('resources/images/sprites/boss/die/')
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

        self.action = 6

        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (877, 610)

    def check_attack_range(self) -> bool:
        """

        :return: true if player is in range for attack
        """

        if (abs(in_game.player_obj.rect.centerx - self.rect.centerx) < 35) and (
                not self.isFlipped and self.rect.centerx >= in_game.player_obj.rect.centerx):
            return True
        if (abs(in_game.player_obj.rect.centerx - self.rect.centerx) < 300) and (
                self.isFlipped and self.rect.centerx <= in_game.player_obj.rect.centerx):
            return True
        return False

    def get_damage(self, val: int) -> None:
        """

        :param val: value of the damage taken by the boss object
        """

        self.hp -= val
        boss_damage_sfx = mixer.Sound(f'resources/sounds/boss/{random.randrange(1, 9)}.wav')
        if self.hp > 0:
            boss_damage_sfx.play()
        else:
            in_game.bossDieSFX.play()
