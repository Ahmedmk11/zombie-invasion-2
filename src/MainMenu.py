from turtle import width
import pygame as pg,sys
from pygame import mixer
pg.init()

inst = False
WIDTH = 1316
HEIGHT = 740

screen = pg.display.set_mode((WIDTH,HEIGHT))
appIcon = pg.image.load('resources/images/app/icon.png')
pg.display.set_icon(appIcon)
pg.display.set_caption("Zombie Invasion: Apocalypse")
clock = pg.time.Clock()
pg.mouse.set_visible(True)
mainScreen = pg.image.load('resources/images/world/level6/6.png')
mainScreen = pg.transform.scale(mainScreen,(1316,740))


# mixer.music.load('MainMenu.wav')
# mixer.music.play(-1)
while True:
    screen.fill((0,0,0))

    playFont = pg.font.Font('resources/fonts/font.ttf',70)
    playText = playFont.render("Play",True,(255,255,255))
    playRect = playText.get_rect(center = (640,300))

    leaderBoardFont = pg.font.Font('resources/fonts/font.ttf',48)
    leaderBoardText = leaderBoardFont.render("Leaderboard",True,(255,255,255))
    leaderBoardRect = leaderBoardText.get_rect(center = (640,360))

    mainFont = pg.font.Font('resources/fonts/font.ttf', 90)
    titleText = mainFont.render("Zombie Invasion",True,(255,255,255))
    titleRect = titleText.get_rect(center = (WIDTH/2,100))

    screen.blit(mainScreen,(0,0))
    screen.blit(playText,playRect)
    screen.blit(leaderBoardText,leaderBoardRect)
    screen.blit(titleText,titleRect)



    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()
        
        if event.type == pg.MOUSEBUTTONDOWN and playRect.collidepoint(event.pos) or event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            pg.quit()
            import InGame
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                inst = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_i:
                inst = False

    if inst:
        instFont = pg.font.Font('resources/fonts/lemonmilk.otf',12)
        instHead = pg.font.Font('resources/fonts/lemonmilk.otf',24)

        instructions = instHead.render("Welcome to Zombie Invasion: Apocalypse",True,(255,255,255))
        instructions1 = instFont.render("Press 'Play' to start the game",True,(255,255,255))
        instructions2 = instFont.render("To play again, press anywhere on the 'Game Over' screen",True,(255,255,255))
        instructions3 = instFont.render("To exit the game, press 'Escape' or close the window",True,(255,255,255))
        instructions4 = instFont.render("Press 'Space' to shoot, 'Left' and 'Right' to move and 'Up' to jump",True,(255,255,255))
        instructions5 = instFont.render("Keep Sky alive as long as you can!",True,(255,255,255))
        instructions6 = instFont.render("Have Fun!",True,(255,255,255))

        screen.blit(instructions,(10,60))
        screen.blit(instructions1,(15,120))
        screen.blit(instructions2,(15,160))
        screen.blit(instructions3,(15,200))
        screen.blit(instructions4,(15,240))
        screen.blit(instructions5,(15,280))
        screen.blit(instructions6,(15,320)) 

    pg.display.update()
    clock.tick(60)
