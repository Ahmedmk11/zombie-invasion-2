import pygame,sys,pickle
from pygame import mixer

pygame.init()
inst = False

screen = pygame.display.set_mode((1316,740))
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)


while True:
    pygame.display.set_caption("Zombie Invasion: Apocalypse")
    pygame.display.update()
    clock.tick(30)
