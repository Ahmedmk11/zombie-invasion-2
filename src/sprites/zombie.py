"""Zombie

Contains the class Zombie

"""

import in_game
import os
import random

import pygame as pg

pg.init()


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


class Zombie(pg.sprite.Sprite):
    """

    A class used to represent the zombie boss object for a final fight in level 6
    This class is the parent class of Boss and passes the following methods:
        * move
        * attack
        * check_damage_range
        * check_attack_range
        * update
        * update_action
    """

    def __init__(self, speed: int, is_boss: bool) -> None:
        super().__init__()
        self.speed = speed
        self.updateTime = pg.time.get_ticks()
        self.frameIndex = 0
        self.attackCoolDown = 0
        self.appearing = True
        self.walking = False
        self.attacking = False
        self.isDying = True
        self.is_boss = is_boss
        random_side = random.randrange(0, 2)

        if random_side == 0:
            random_xpos = range(-20, 180)
            self.isFlipped = True
        else:
            random_xpos = range(1136, 1336)
            self.isFlipped = False

        if not self.isFlipped:
            self.action = 6
        elif self.isFlipped:
            self.action = 7

        self.hp = 10
        self.walkLeft = make_animation('resources/images/sprites/zombies/walk/')
        self.walkRight = make_animation_flip('resources/images/sprites/zombies/walk/')
        self.idleLeft = make_animation('resources/images/sprites/zombies/idle/')
        self.idleRight = make_animation_flip('resources/images/sprites/zombies/idle/')
        self.attackLeft = make_animation('resources/images/sprites/zombies/attack/')
        self.attackRight = make_animation_flip('resources/images/sprites/zombies/attack/')
        self.appearLeft = make_animation('resources/images/sprites/zombies/appear/')
        self.appearRight = make_animation_flip('resources/images/sprites/zombies/appear/')
        self.dieLeft = make_animation('resources/images/sprites/zombies/die/')
        self.dieRight = make_animation_flip('resources/images/sprites/zombies/die/')
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

        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.choice(random_xpos), 610)

    def move(self) -> None:
        """

        This function is responsible for moving the zombie
        """

        if not self.appearing:
            if self.walking and not self.hp <= 0:
                if not self.isFlipped:
                    self.update_action(2)
                elif self.isFlipped:
                    self.update_action(3)

            if not self.isFlipped:
                self.rect.centerx -= self.speed
            if self.isFlipped:
                self.rect.centerx += self.speed

    def attack(self) -> None:
        """

        This function is responsible for triggering the attack animation
        """

        if self.attacking and not self.hp <= 0:
            if not self.isFlipped:
                self.update_action(4)
            if self.isFlipped:
                self.update_action(5)

    def check_attack_range(self) -> bool:
        """

        :return: true if player is in range for attack
        """

        if (abs(in_game.player_obj.rect.centerx - self.rect.centerx) < 35) and (
                not self.isFlipped and self.rect.centerx >= in_game.player_obj.rect.centerx):
            return True
        if (abs(in_game.player_obj.rect.centerx - self.rect.centerx) < 70) and (
                self.isFlipped and self.rect.centerx <= in_game.player_obj.rect.centerx):
            return True
        return False

    def check_damage_range(self) -> bool:
        """

        :return: true if player is in range to take damage from being close to zombies
        """

        if abs(in_game.player_obj.rect.centerx - self.rect.centerx) < 35:
            return True
        if abs(in_game.player_obj.rect.centerx - self.rect.centerx) < 65:
            return True
        return False

    def update(self) -> None:
        """

        This function updates the zombie object every frame during the game
        """

        if self.attacking:
            animation_cooldown = 125
        elif self.appearing and not self.is_boss:
            animation_cooldown = 100
        elif self.appearing and self.is_boss:
            animation_cooldown = 105
        elif self.hp <= 0 and not self.is_boss:
            animation_cooldown = 60
        elif self.hp <= 0 and self.is_boss:
            animation_cooldown = 100
        else:
            animation_cooldown = 90

        self.image = self.anime[self.action][self.frameIndex]

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()

            if self.appearing and self.frameIndex == len(self.anime[self.action]) - 1:
                self.appearing = False
                self.walking = True
                if not self.is_boss:
                    self.rect.bottom = 605
                else:
                    self.rect.bottom = 583

            else:
                self.frameIndex += 1

            if self.frameIndex == len(self.anime[self.action]) - 1 and self.hp <= 0 and self.isDying:
                self.isDying = False
                self.kill()
            else:
                self.frameIndex += 1

            if self.attacking and self.frameIndex == len(self.anime[self.action]) - 1:
                if not self.is_boss:
                    in_game.player_obj.get_damage(10)
                    in_game.hitSFX.play()
                else:
                    in_game.player_obj.get_damage(50)
                    in_game.hitSFX.play()

            if pg.sprite.spritecollide(in_game.player_group.sprite, in_game.zombies_group,
                                       False) and self.check_damage_range():
                in_game.player_group.sprite.get_damage(0.5)

        if self.frameIndex >= len(self.anime[self.action]):
            self.frameIndex = 0

        if in_game.alive and not self.attacking:
            self.move()

        if not self.appearing:
            if self.check_attack_range() and in_game.player_obj.hp > 0:
                self.attacking = True
                self.walking = False
                self.attack()
            else:
                self.attacking = False
                self.walking = True

        if self.attackCoolDown > 0:
            self.attackCoolDown -= 1

        if not self.is_boss and (self.rect.centerx >= 1336 or self.rect.centerx <= -20):
            self.kill()

        if self.is_boss:

            if in_game.player_obj.rect.left >= self.rect.right:
                right_dist = in_game.player_obj.rect.left - self.rect.right
                left_dist = (in_game.WIDTH - in_game.player_obj.rect.right) + self.rect.left
            else:
                right_dist = in_game.player_obj.rect.left + (in_game.WIDTH - self.rect.right)
                left_dist = self.rect.left - in_game.player_obj.rect.right

            if not self.isFlipped:
                if right_dist <= left_dist and not right_dist < 0:
                    self.isFlipped = True
            else:
                if right_dist > left_dist and not left_dist < 0:
                    self.isFlipped = False

            if self.hp <= 0:
                in_game.alive = False
                if not self.isFlipped:
                    in_game.isMovingLeft = False
                    in_game.isMovingRight = False
                    in_game.isIdleLeft = True
                    in_game.isIdleRight = False
                    in_game.isShootingLeft = False
                    in_game.isShootingRight = False
                    in_game.isDeadLeft = False
                if self.isFlipped:
                    in_game.isMovingLeft = False
                    in_game.isMovingRight = False
                    in_game.isIdleLeft = False
                    in_game.isIdleRight = True
                    in_game.isShootingLeft = False
                    in_game.isShootingRight = False
                    in_game.isDeadRight = False

        if not self.is_boss or (self.is_boss and self.hp > 0):
            if not self.isFlipped and not in_game.alive:
                self.update_action(0)
            if self.isFlipped and not in_game.alive:
                self.update_action(1)

    def update_action(self, new_action: int) -> None:
        """

        :param new_action: a new action to replace the old one
        """

        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()
