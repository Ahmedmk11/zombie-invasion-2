import pygame as pg
from sprites import Zombie as zm
import InGame

class Boss(zm.Zombie): # inherited: move, update_action, attack
    def __init__(self):
        zm.Zombie.__init__(self,1250,1,False, True)

    def checkAttackRange(self):
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 350) and (not self.isFlipped and self.rect.centerx > InGame.player.rect.centerx):
            return True
        if (abs(InGame.player.rect.centerx - self.rect.centerx) < 350) and (self.isFlipped and self.rect.centerx < InGame.player.rect.centerx):
            return True
        return False