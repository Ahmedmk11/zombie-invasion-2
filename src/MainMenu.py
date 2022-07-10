import pygame as pg,sys
from pygame import mixer
pg.init()

inst = False

screen = pg.display.set_mode((1316,740))
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

    playFont = pg.font.Font('resources/fonts/Starjedi.ttf',60)
    playText = playFont.render("Play",True,(255,255,255))
    playRect = playText.get_rect(center = (640,300))

    leaderBoardFont = pg.font.Font('resources/fonts/Starjedi.ttf',38)
    leaderBoardText = leaderBoardFont.render("Leaderboard",True,(255,255,255))
    leaderBoardRect = leaderBoardText.get_rect(center = (640,360))

    screen.blit(mainScreen,(0,0))
    screen.blit(playText,playRect)
    screen.blit(leaderBoardText,leaderBoardRect)



    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if playRect.collidepoint(event.pos):
                pg.quit()
                import InGame
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                inst = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_i:   
                inst = False

    # if inst:
        # instructions_rect = pg.draw.rect(screen,(57,61,71),(0,200,550,400))
        # instructions = playFont.render("Welcome to Zombie Invasion!",True,(255,255,255))
        # instructions1 = playFont.render("Press 'Play' to start the game",True,(255,255,255))
        # instructions2 = playFont.render("To play again, press anywhere on the 'Game Over' screen",True,(255,255,255))
        # instructions3 = playFont.render("To exit the game, press 'Escape' or close the window",True,(255,255,255))
        # instructions4 = playFont.render("Press 'Space' to shoot, 'Left' and 'Right' to move and 'Up' to jump",True,(255,255,255))
        # instructions5 = playFont.render("Keep Sky alive as long as you can!",True,(255,255,255))
        # instructions6 = playFont.render("Have Fun!",True,(255,255,255))

        # screen.blit(instructions,(10,220))
        # screen.blit(instructions1,(15,280))
        # screen.blit(instructions2,(15,320))
        # screen.blit(instructions3,(15,360))
        # screen.blit(instructions4,(15,400))
        # screen.blit(instructions5,(15,440))
        # screen.blit(instructions6,(15,480)) 

    pg.display.update()
    clock.tick(60)
