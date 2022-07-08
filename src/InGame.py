import pygame as pg, math, random, sys
from pygame import mixer 
pg.init()

WIDTH = 1316
HEIGHT = 740


screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
pg.mouse.set_visible(True)
mainScreen = pg.image.load('resources/images/world/level1/1.png')
mainScreen = pg.transform.scale(mainScreen,(1316,740))

def main():
    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                mixer.music.stop()
                running = False
        

        screen.blit(mainScreen,(0,0))

        pg.display.update()
        appIcon = pg.image.load('resources/images/app/icon.png')
        pg.display.set_icon(appIcon)
        clock.tick(60)