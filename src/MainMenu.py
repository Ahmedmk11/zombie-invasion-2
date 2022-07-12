from pygame import mixer
import pygame as pg, sys, pickle
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
mainScreen = pg.transform.scale(mainScreen,(WIDTH,HEIGHT))

up = pg.image.load("resources/images/app/up.png")
right = pg.image.load("resources/images/app/right.png")
left = pg.image.load("resources/images/app/left.png")
s = pg.image.load("resources/images/app/s.png")
q = pg.image.load("resources/images/app/q.png")
e = pg.image.load("resources/images/app/e.png")

cursor = pg.image.load('resources/images/app/cursor.png')
cursorRect = cursor.get_rect()
pg.mouse.set_visible(False)

MAX_X, MAX_Y = screen.get_size()

playFont1 = pg.font.Font('resources/fonts/font.ttf',70)
playFont2 = pg.font.Font('resources/fonts/font.ttf',70)
leaderBoardFont = pg.font.Font('resources/fonts/font.ttf',30)

# mixer.music.load('MainMenu.wav')
# mixer.music.play(-1)

while True:
    screen.fill((0,0,0))

    playText1 = playFont1.render("Story Mode",True,(255,255,255))
    playRect1 = playText1.get_rect(center = (640,280))

    playText2 = playFont2.render("Survival Mode",True,(255,255,255))
    playRect2 = playText2.get_rect(center = (640,360))

    leaderBoardText = leaderBoardFont.render("Leaderboard",True,(255,255,255))
    leaderBoardRect = leaderBoardText.get_rect(center = (1190,30))

    if playRect1.collidepoint((pg.mouse.get_pos()[0],pg.mouse.get_pos()[1] - 12)):
        playFont1 = pg.font.Font('resources/fonts/font.ttf',int(80*1.1))
    else:
        playFont1 = pg.font.Font('resources/fonts/font.ttf',80)

    if playRect2.collidepoint((pg.mouse.get_pos()[0],pg.mouse.get_pos()[1] - 12)):
        playFont2 = pg.font.Font('resources/fonts/font.ttf',int(80*1.1))
    else:
        playFont2 = pg.font.Font('resources/fonts/font.ttf',80)
    
    if leaderBoardRect.collidepoint((pg.mouse.get_pos()[0],pg.mouse.get_pos()[1] - 12)):
        leaderBoardFont = pg.font.Font('resources/fonts/font.ttf',int(40*1.1))
    else:
        leaderBoardFont = pg.font.Font('resources/fonts/font.ttf',40)

    mainFont = pg.font.Font('resources/fonts/font.ttf', 90)
    titleText = mainFont.render("Zombie Invasion",True,(255,255,255))
    titleRect = titleText.get_rect(center = (WIDTH/2,100))

    cursorRect.center = pg.mouse.get_pos()
        
    screen.blit(mainScreen,(0,0))
    screen.blit(playText1,playRect1)
    screen.blit(playText2,playRect2)
    screen.blit(leaderBoardText,leaderBoardRect)
    screen.blit(titleText,titleRect)


    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and (playRect1.collidepoint(event.pos) or playRect2.collidepoint(event.pos)):
            if playRect1.collidepoint(event.pos):
                with open("mode.pickle", "wb") as modes:
                    pickle.dump(1, modes)
            else:
                with open("mode.pickle", "wb") as modes:
                    pickle.dump(2, modes)
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
        instructions1 = instFont.render("Press            to move and       to jump",True,(255,255,255))
        instructions2 = instFont.render("Press       and       to shoot at an angle and       to shoot horizontally",True,(255,255,255))
        instructions3 = instFont.render("Difficulty keeps increasing each level in 'Story' and as time progress in 'Survival'",True,(255,255,255))
        instructions4 = instFont.render("Have Fun!",True,(255,255,255))

        screen.blit(left,(62,580))
        screen.blit(right,(78,580))
        screen.blit(up,(200,580))
        screen.blit(q,(60,622))
        screen.blit(e,(115,622))
        screen.blit(s,(330,622))
        screen.blit(instructions,(10,520))
        screen.blit(instructions1,(15,580))
        screen.blit(instructions2,(15,620))
        screen.blit(instructions3,(15,660))
        screen.blit(instructions4,(15,700))
    
    x, y = pg.mouse.get_pos()
    if x > 0 and x < MAX_X - 1 and y > 0 and y < MAX_Y - 1:
        screen.blit(cursor, cursorRect)
        
    pg.display.update()
    clock.tick(60)
