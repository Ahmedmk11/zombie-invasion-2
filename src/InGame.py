import pygame as pg, math, random, sys
from sprites import Player as pl
from sprites import Platform as pt
from pygame import mixer 
pg.init()

WIDTH = 1316
HEIGHT = 740

screen = pg.display.set_mode((WIDTH,HEIGHT))
appIcon = pg.image.load('resources/images/app/icon.png')
pg.display.set_icon(appIcon)
pg.display.set_caption("Zombie Invasion: Apocalypse")
clock = pg.time.Clock()
pg.mouse.set_visible(True)
mainScreen = pg.image.load('resources/images/world/level1/1.png')
mainScreen = pg.transform.scale(mainScreen,(1316,740))


player = pl.Player(screen)
player_group = pg.sprite.GroupSingle()
player_group.add(player)

platform = pt.Platform()
platform_group = pg.sprite.GroupSingle()
platform_group.add(platform)

def main():
    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                mixer.music.stop()
                break
        

        screen.blit(mainScreen,(0,0))
        platform_group.draw(screen)
        pg.display.update()
        clock.tick(60)