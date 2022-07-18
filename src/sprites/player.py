"""Player

Contains the class Player

"""

import in_game
import os
import pygame as pg
from pygame import Vector2

from sprites import bullet

pg.init()

WIDTH = 1316
HEIGHT = 526
ACCELERATION = 0.7
FRICTION = -0.12
GRAVITY = 11


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


class Player(pg.sprite.Sprite):
    """

    A class used to represent the player object
    This class defines the following methods:
        * move
        * jump
        * shoot
        * get_damage
        * die
        * update
        * update_action
    """

    def __init__(self) -> None:
        super().__init__()
        self.bullet = None
        self.updateTime = pg.time.get_ticks()
        self.frameIndex = 0
        if in_game.level == 6:
            in_game.isIdleLeft = False
        if in_game.level != 6:
            in_game.isIdleRight = False
        in_game.isShootingLeft = False
        in_game.isShootingRight = False
        in_game.isMovingLeft = False
        in_game.isMovingRight = False
        in_game.isShootingRightUp = False
        in_game.isShootingLeftUp = False
        self.hp = 200
        self.vel_vec = Vector2(0, 0)
        self.acc_vec = Vector2(0, 0)
        self.isShooting = False
        self.isDead = False
        self.isJumping = False
        self.isIdle = True

        if in_game.level == 6:
            self.action = 1
            self.isFlipped = True
            self.pos = Vector2(438, 540)
            self.direction = -1
        else:
            self.action = 0
            self.isFlipped = False
            self.pos = Vector2(WIDTH / 2, 540)
            self.direction = 1

        self.shootingCoolDown = 0
        self.shootingCoolDownUp = 0
        self.currScore = 0

        self.walkLeft = make_animation('resources/images/sprites/heroine/walk/')
        self.walkRight = make_animation_flip('resources/images/sprites/heroine/walk/')
        self.idleLeft = make_animation('resources/images/sprites/heroine/idle/')
        self.idleRight = make_animation_flip('resources/images/sprites/heroine/idle/')
        self.shootLeft = make_animation('resources/images/sprites/heroine/shoot/')
        self.shootRight = make_animation_flip('resources/images/sprites/heroine/shoot/')
        self.dieLeft = make_animation('resources/images/sprites/heroine/die/')
        self.dieRight = make_animation_flip('resources/images/sprites/heroine/die/')
        self.anime = []
        self.anime.append(self.idleLeft)
        self.anime.append(self.idleRight)
        self.anime.append(self.walkLeft)
        self.anime.append(self.walkRight)
        self.anime.append(self.shootLeft)
        self.anime.append(self.shootRight)
        self.anime.append(self.dieLeft)
        self.anime.append(self.dieRight)

        self.image = self.anime[self.action][self.frameIndex]
        self.rect = self.image.get_rect()

    def move(self) -> None:
        """

        This method is responsible for moving the player
        """

        self.acc_vec = Vector2(0, ACCELERATION)
        if in_game.isMovingLeft:
            self.acc_vec.x = -ACCELERATION
            self.isFlipped = False
            self.direction = 1

        if in_game.isMovingRight:
            self.acc_vec.x = ACCELERATION
            self.isFlipped = True
            self.direction = -1

        self.acc_vec.x += self.vel_vec.x * FRICTION
        self.vel_vec += self.acc_vec
        self.pos += self.vel_vec + 0.5 * self.acc_vec

        self.rect.midbottom = self.pos

        hits = pg.sprite.spritecollide(in_game.player_group.sprite, in_game.platform_group, False)
        if hits:
            self.pos.y = hits[0].rect.top
            self.vel_vec.y = 0

    def jump(self) -> None:
        """

        This method allows the player to jump
        """

        self.rect.y += 1
        hits = pg.sprite.spritecollide(in_game.player_group.sprite, in_game.platform_group, False)
        self.rect.y -= -1
        if hits:
            in_game.jumpSFX.play()
            self.vel_vec.y = -17

    def shoot(self, angle: bool) -> None:
        """

        :param angle: boolean to pass to the bullet object to check if it's fired at an angle or horizontal
        """

        if self.shootingCoolDown == 0:
            self.bullet = bullet.Bullet(self.rect.centerx - (0.5 * self.direction * self.rect.size[0]),
                                        self.rect.centery - 12, self.direction, angle)
            in_game.bullet_group.add(self.bullet)
            self.shootingCoolDown = 15

    def get_damage(self, val: int) -> None:
        """

        :param val: the amount of damage the player received
        """

        self.hp -= val

    def die(self) -> None:
        """

        This method is responsible for triggering the dying animations
        """

        in_game.alive = False
        zombie_exists = 'zombie' in locals() or 'zombie' in globals()
        if zombie_exists:
            if not in_game.zombie.isFlipped:
                in_game.isIdleLeftZombie = True
            else:
                in_game.isIdleRightZombie = True
        if not self.isFlipped:
            in_game.isMovingLeft = False
            in_game.isMovingRight = False
            in_game.isIdleLeft = False
            in_game.isIdleRight = False
            in_game.isShootingLeft = False
            in_game.isShootingRight = False
            in_game.isDeadLeft = True
        if self.isFlipped:
            in_game.isMovingLeft = False
            in_game.isMovingRight = False
            in_game.isIdleLeft = False
            in_game.isIdleRight = False
            in_game.isShootingLeft = False
            in_game.isShootingRight = False
            in_game.isDeadRight = True

    def update(self) -> None:
        """

        This method updates the player object every frame during the game
        """

        animation_cooldown = 75
        self.image = self.anime[self.action][self.frameIndex]

        if pg.time.get_ticks() - self.updateTime >= animation_cooldown:
            self.updateTime = pg.time.get_ticks()
            if self.hp <= 0 and self.frameIndex == len(self.anime[self.action]) - 1:
                self.frameIndex = len(self.anime[self.action]) - 1
            else:
                self.frameIndex += 1

        if self.frameIndex >= len(self.anime[self.action]) and in_game.alive:
            self.frameIndex = 0

        if self.frameIndex >= len(self.anime[self.action]) and not in_game.alive and self.hp > 0:
            self.frameIndex = 0

        if self.shootingCoolDown > 0:
            self.shootingCoolDown -= 1
        if self.shootingCoolDownUp > 0:
            self.shootingCoolDownUp -= 1

        in_game.screen.blit(self.image, self.rect)

    def update_action(self, new_action: int) -> None:
        """

        :param new_action: a new action to replace the old one
        """

        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()
