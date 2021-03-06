"""InGame

Main game file that controls all GUI and game logic and contains the game loops
Defined functions:
    * hover - used to check if user hovers on a rectangle and scales the text x1.1
    * draw_rect_alpha - used to draw transparent rectangles
    * level_up - returns a new player object after clearing all sprite groups
    * game_over - returns the text to be displayed when player wins or loses and kills off all enemy sprites still alive
    * main_game - contains a part of the game loop for better readability

    ** To start the game run the __init__.py file in the same directory as this file

"""

import datetime
import pathlib
import pickle
import random
import itertools
import sys
from operator import itemgetter
from typing import Any

import pygame as pg
from pygame import mixer
from pygame.rect import Rect, RectType
from pygame.surface import Surface, SurfaceType

from sprites import boss
from sprites import dragon
from sprites import game_platform
from sprites import player
from sprites import zombie

pg.init()

window = 1
mode = 1
WIDTH = 1316
HEIGHT = 740
windowFlag = True
mainSFXFlag = False

buttonSFX = mixer.Sound('resources/sounds/button.wav')
typeSFX = mixer.Sound('resources/sounds/type.wav')
backSpaceSFX = mixer.Sound('resources/sounds/backspace.wav')
closeSFX = mixer.Sound('resources/sounds/save_close.wav')
openSFX = mixer.Sound('resources/sounds/save_open.wav')
winSFX = mixer.Sound('resources/sounds/win.wav')
loseSFX = mixer.Sound('resources/sounds/lose.wav')
levelSFX = mixer.Sound('resources/sounds/level_up.wav')
jumpSFX = mixer.Sound('resources/sounds/jump.wav')
hitSFX = mixer.Sound('resources/sounds/player_hit.wav')
bulletSFX = mixer.Sound('resources/sounds/bullet.wav')
lifeLostSFX = mixer.Sound('resources/sounds/life_lost.wav')
zombieDieSFX = mixer.Sound('resources/sounds/zombie_die.wav')
fireballSFX = mixer.Sound('resources/sounds/fireball.wav')
dragonDieSFX = mixer.Sound('resources/sounds/dragon_die.wav')
bossDieSFX = mixer.Sound('resources/sounds/boss/boss_die.wav')


def hover(rec: pg.Rect, size: int, fnt_name: str, ext: str) -> pg.font:
    """

    :param rec: the rectangle that the player hovers on
    :param size: default font size for text
    :param fnt_name: font name in directory fonts/
    :param ext: font file extension
    :return: the default font or the scaled font if mouse hovers on it
    """

    if rec.collidepoint((pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] - 12)):
        fnt = pg.font.Font(f'resources/fonts/{fnt_name}.{ext}', int(size * 1.1))
    else:
        fnt = pg.font.Font(f'resources/fonts/{fnt_name}.{ext}', size)
    return fnt


def draw_rect_alpha(surface: pg.Surface, color: pg.Color, rect: pg.Rect) -> None:
    """
    
    :param surface: the surface that will blit the rectrangle
    :param color: the color of the rectangle
    :param rect: the rectangle that will be drawn (position of the colored rectangle)
    This function is used for drawing rectangles with an alpha value: https://stackoverflow.com/a/64630102/15972847
    """

    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def level_up() -> player.Player:
    """

    :return: a new player after emptying all groups
    """

    levelSFX.play()
    bullet_group.empty()
    fireball_group.empty()
    zombies_group.empty()
    dragon_group.empty()
    player_group.empty()
    plr = player.Player()
    player_group.add(plr)
    return plr


def game_over(is_one_level: bool, rtime_zero: bool) -> tuple[Surface | SurfaceType, Rect | RectType | Any, bool]:
    """

    :param rtime_zero: boolean to check if the round timer is zero
    :param is_one_level: boolean to check if the game was story mode or just one level
    :return: a text "Game Over" or "You Won" and the text's rectangle and a boolean to check if game over
    """

    bullet_group.empty()
    fireball_group.empty()

    game_over_font = pg.font.Font('resources/fonts/game_over.ttf', 180)

    txt = game_over_font.render('', True, (0, 0, 0))
    txt_rect = txt.get_rect()

    if lives == 0:
        if loseFlagSFX:
            loseSFX.play()
        txt = game_over_font.render("Game Over", True, (255, 255, 255))
        txt_rect = txt.get_rect(center=(653, 243))
    if bossExists:
        if boss_obj.hp <= 0:
            txt = game_over_font.render("You Won", True, (255, 255, 255))
            txt_rect = txt.get_rect(center=(653, 243))
            for zm in zombies_group:
                zm.hp = 0
            for dr in dragon_group:
                dr.hp = 0
    if is_one_level and rtime_zero:
        txt = game_over_font.render("You Won", True, (255, 255, 255))
        txt_rect = txt.get_rect(center=(653, 243))
        for zm in zombies_group:
            zm.hp = 0
        for dr in dragon_group:
            dr.hp = 0

    is_gm_over = True
    return txt, txt_rect, is_gm_over


def main_game() -> None:
    """

    used in the game loop for a cleaner code and a shorter while loop
    """

    pg.draw.rect(screen, (255, 255, 255), (58, 35, 200, 10))
    pg.draw.rect(screen, (191, 33, 48), (58, 35, player_obj.hp, 10))
    screen.blit(heart, (0, 2))

    if bossExists:
        if level == 6 and boss_obj.hp > 0:
            pg.draw.rect(screen, (105, 105, 105), (405, 32, 506, 26))
            pg.draw.rect(screen, (34, 139, 34), (408, 35, boss_obj.hp / 6, 20))
            pg.draw.rect(screen, (105, 105, 105), (658, 35, 6, 20))
            screen.blit(bossHead, bossHead_rect)

    bullet_group.draw(screen)
    fireball_group.draw(screen)
    zombies_group.draw(screen)
    dragon_group.draw(screen)
    boss_group.draw(screen)
    player_group.draw(screen)
    platform_group.draw(screen)

    bullet_group.update()
    fireball_group.update()
    zombies_group.update()
    dragon_group.update()
    boss_group.update()
    player_group.update()

    if isIdleLeft:
        player_obj.update_action(0)
    if isIdleRight:
        player_obj.update_action(1)
    if isMovingLeft:
        player_obj.update_action(2)
    if isMovingRight:
        player_obj.update_action(3)
    if isShootingLeft or isShootingLeftUp:
        player_obj.update_action(4)
    if isShootingRight or isShootingRightUp:
        player_obj.update_action(5)
    if isDeadLeft:
        player_obj.update_action(6)
    if isDeadRight:
        player_obj.update_action(7)

    player_obj.move()

    if isShootingLeft or isShootingRight:
        player_obj.shoot(False)

    if isShootingLeftUp or isShootingRightUp:
        player_obj.shoot(True)

    if player_obj.pos.x > WIDTH:
        player_obj.pos.x = 0
    if player_obj.pos.x < 0:
        player_obj.pos.x = WIDTH

    if bossExists:
        if level == 6:
            if boss_obj.rect.centerx >= WIDTH:
                boss_obj.rect.centerx = 0
            if boss_obj.rect.centerx < 0:
                boss_obj.rect.centerx = WIDTH


while True:

    levels = 0
    oneLevel = False

    if window == 1:

        if not mainSFXFlag:
            pg.mixer.music.stop()
            pg.mixer.music.load('resources/sounds/music/mainmenu.wav')
            pg.mixer.music.play(-1)

        mainSFXFlag = False
        inst = False
        isToggled = False

        appIcon = pg.image.load('resources/images/app/icon.png')
        mainScreen = pg.image.load('resources/images/world/6.png')
        up = pg.image.load("resources/images/app/up.png")
        right = pg.image.load("resources/images/app/right.png")
        left = pg.image.load("resources/images/app/left.png")
        s = pg.image.load("resources/images/app/s.png")
        w = pg.image.load("resources/images/app/w.png")
        cursor = pg.image.load('resources/images/app/cursor.png')
        infoSymbol = pg.image.load('resources/images/app/help.png')

        playFont1 = pg.font.Font('resources/fonts/font.ttf', 80)
        playFont2 = pg.font.Font('resources/fonts/font.ttf', 80)
        leaderBoardFont = pg.font.Font('resources/fonts/font.ttf', 40)
        levelsFont = pg.font.Font('resources/fonts/font.ttf', 40)
        quitFont = pg.font.Font('resources/fonts/font.ttf', 30)
        mainFont = pg.font.Font('resources/fonts/font.ttf', 90)
        instFont = pg.font.Font('resources/fonts/lemonmilk.otf', 12)
        instHead = pg.font.Font('resources/fonts/lemonmilk.otf', 24)
        level1Font = pg.font.Font('resources/fonts/font.ttf', 32)
        level2Font = pg.font.Font('resources/fonts/font.ttf', 32)
        level3Font = pg.font.Font('resources/fonts/font.ttf', 32)
        level4Font = pg.font.Font('resources/fonts/font.ttf', 32)
        level5Font = pg.font.Font('resources/fonts/font.ttf', 32)
        level6Font = pg.font.Font('resources/fonts/font.ttf', 32)

        pg.display.set_caption("Zombie Invasion: Apocalypse")
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_icon(appIcon)
        clock = pg.time.Clock()
        mainScreen = pg.transform.scale(mainScreen, (WIDTH, HEIGHT))
        pg.mouse.set_visible(False)

        titleText = mainFont.render("Zombie Invasion", True, (255, 255, 255))
        instructions = instHead.render("Welcome to Zombie Invasion: Apocalypse", True, (255, 255, 255))
        instructions1 = instFont.render("Press            to move and       to jump", True, (255, 255, 255))
        instructions2 = instFont.render("Press       to shoot at an angle and       to shoot horizontally", True,
                                        (255, 255, 255))
        instructions3 = instFont.render(
            "Difficulty keeps increasing each level in 'Story' and as time progress in 'Survival'", True,
            (255, 255, 255))
        instructions4 = instFont.render("Have Fun!", True, (255, 255, 255))

        MAX_X, MAX_Y = screen.get_size()
        cursorRect = cursor.get_rect()
        titleRect = titleText.get_rect(center=(WIDTH / 2, 100))
        helpRect = infoSymbol.get_rect(center=(50, 710))

        while True:
            screen.fill((0, 0, 0))
            cursorRect.center = pg.mouse.get_pos()

            playText1 = playFont1.render("Story", True, (255, 255, 255))
            playText2 = playFont2.render("Survival", True, (255, 255, 255))
            leaderBoardText = leaderBoardFont.render("Leaderboard", True, (255, 255, 255))
            quitText = quitFont.render("Quit", True, (255, 255, 255))
            levelsText = levelsFont.render("Levels", True, (255,255,255))
            level1Text = level1Font.render("Level 1", True, (255,255,255))
            level2Text = level2Font.render("Level 2", True, (255,255,255))
            level3Text = level3Font.render("Level 3", True, (255,255,255))
            level4Text = level4Font.render("Level 4", True, (255,255,255))
            level5Text = level5Font.render("Level 5", True, (255,255,255))
            level6Text = level6Font.render("Level 6", True, (255,255,255))

            playRect1 = playText1.get_rect(center=(640, 280))
            playRect2 = playText2.get_rect(center=(640, 360))
            leaderBoardRect = leaderBoardText.get_rect(center=(1190, 30))
            quitRect = quitText.get_rect(center=(1250, 700))
            levelsRect = levelsText.get_rect(center=(80,40))
            level1Rect = level1Text.get_rect(center=(80, 100))
            level2Rect = level2Text.get_rect(center=(80, 160))
            level3Rect = level3Text.get_rect(center=(80, 220))
            level4Rect = level4Text.get_rect(center=(80, 280))
            level5Rect = level5Text.get_rect(center=(80, 340))
            level6Rect = level6Text.get_rect(center=(80, 400))
            toggledLevelsRect = pg.rect.Rect(10, 72, 150, 355)

            playFont1 = hover(playRect1, 80, "font", "ttf")
            playFont2 = hover(playRect2, 80, "font", "ttf")
            leaderBoardFont = hover(leaderBoardRect, 40, "font", "ttf")
            quitFont = hover(quitRect, 30, "font", "ttf")
            levelsFont = hover(levelsRect, 40, "font", "ttf")
            level1Font = hover(level1Rect, 32, "font", "ttf")
            level2Font = hover(level2Rect, 32, "font", "ttf")
            level3Font = hover(level3Rect, 32, "font", "ttf")
            level4Font = hover(level4Rect, 32, "font", "ttf")
            level5Font = hover(level5Rect, 32, "font", "ttf")
            level6Font = hover(level6Rect, 32, "font", "ttf")

            screen.blit(mainScreen, (0, 0))
            screen.blit(playText1, playRect1)
            screen.blit(playText2, playRect2)
            screen.blit(leaderBoardText, leaderBoardRect)
            screen.blit(quitText, quitRect)
            screen.blit(levelsText, levelsRect)
            screen.blit(titleText, titleRect)

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (
                        event.type == pg.MOUSEBUTTONUP and (quitRect.collidepoint(event.pos))):
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONUP and (
                        playRect1.collidepoint(event.pos) or playRect2.collidepoint(event.pos)):
                    buttonSFX.play()
                    if playRect1.collidepoint(event.pos):
                        mode = 1
                    else:
                        mode = 2
                    windowFlag = False
                    window = 2
                    break

                if event.type == pg.MOUSEBUTTONUP and leaderBoardRect.collidepoint(event.pos):
                    buttonSFX.play()

                    windowFlag = False
                    window = 3
                    break

                if event.type == pg.MOUSEBUTTONUP and level1Rect.collidepoint(event.pos):
                    buttonSFX.play()
                    levels = 1
                    oneLevel = True
                    mode = 1
                    windowFlag = False
                    window = 2
                    break

                if event.type == pg.MOUSEBUTTONUP and level2Rect.collidepoint(event.pos):
                    buttonSFX.play()
                    levels = 2
                    oneLevel = True
                    mode = 1
                    windowFlag = False
                    window = 2
                    break

                if event.type == pg.MOUSEBUTTONUP and level3Rect.collidepoint(event.pos):
                    buttonSFX.play()
                    levels = 3
                    oneLevel = True
                    mode = 1
                    windowFlag = False
                    window = 2
                    break
                
                if event.type == pg.MOUSEBUTTONUP and level4Rect.collidepoint(event.pos):
                    buttonSFX.play()
                    levels = 4
                    oneLevel = True
                    mode = 1
                    windowFlag = False
                    window = 2
                    break
                
                if event.type == pg.MOUSEBUTTONUP and level5Rect.collidepoint(event.pos):
                    buttonSFX.play()
                    levels = 5
                    oneLevel = True
                    mode = 1
                    windowFlag = False
                    window = 2
                    break
                
                if event.type == pg.MOUSEBUTTONUP and level6Rect.collidepoint(event.pos):
                    buttonSFX.play()
                    levels = 6
                    oneLevel = True
                    mode = 1
                    windowFlag = False
                    window = 2
                    break
                
                if event.type == pg.MOUSEBUTTONUP and levelsRect.collidepoint(event.pos):
                    buttonSFX.play()
                    isToggled = not isToggled

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_i:
                        buttonSFX.play()
                        inst = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_i:
                        inst = False

            if not windowFlag:
                windowFlag = True
                break

            if inst:
                screen.blit(left, (62, 580))
                screen.blit(right, (78, 580))
                screen.blit(up, (200, 580))
                screen.blit(w, (62, 622))
                screen.blit(s, (274, 622))
                screen.blit(instructions, (10, 520))
                screen.blit(instructions1, (15, 580))
                screen.blit(instructions2, (15, 620))
                screen.blit(instructions3, (15, 660))
                screen.blit(instructions4, (15, 700))
            else:
                screen.blit(infoSymbol, helpRect)

            if isToggled:
                draw_rect_alpha(screen, (38,37,38), toggledLevelsRect)
                screen.blit(level1Text, level1Rect)
                screen.blit(level2Text, level2Rect)
                screen.blit(level3Text, level3Rect)
                screen.blit(level4Text, level4Rect)
                screen.blit(level5Text, level5Rect)
                screen.blit(level6Text, level6Rect)

            x, y = pg.mouse.get_pos()
            if 0 < x < MAX_X - 1 and 0 < y < MAX_Y - 1:
                screen.blit(cursor, cursorRect)
            pg.display.update()
            clock.tick(60)

    if window == 2:

        pg.mixer.music.stop()
        pg.mixer.music.load('resources/sounds/music/ingame.wav')
        pg.mixer.music.play(-1)
        lives = 3
        level = 1
        remaining_mins = 0
        remaining_secs = 59
        rtime = 59
        dragonFreq = 3000
        if mode == 1:
            zombieSpeed = 2
        elif mode == 2:
            zombieSpeed = 1
        zombieFreq = 600
        nameText = "Name Here"
        frameI = 0

        save = False
        zombiesWave = True
        dragonsWave = False
        isGameOver = False
        bossExists = False
        active = False
        checkpoint = True
        checkpointFlag = False
        alive = True
        isIdleLeft = True
        isIdleRight = False
        isMovingLeft = False
        isMovingRight = False
        isShootingLeft = False
        isShootingRight = False
        isShootingLeftUp = False
        isShootingRightUp = False
        isDeadLeft = False
        isDeadRight = False
        timeFlag = True
        winFlagSFX = True
        loseFlagSFX = True
        winFlag = True
        isWin = False
        rickFlag = False
        noTimer = False
        zero = False

        rrlist = []
        livesList = []
        livesListRect = []
        zombieEvent = pg.USEREVENT
        dragonEvent = pg.USEREVENT
        zombies_group = pg.sprite.Group()
        dragon_group = pg.sprite.Group()
        bullet_group = pg.sprite.Group()
        fireball_group = pg.sprite.Group()
        boss_group = pg.sprite.GroupSingle()
        platform_group = pg.sprite.GroupSingle()
        player_group = pg.sprite.GroupSingle()
        platform = game_platform.Platform()
        player_obj = player.Player()

        heart = pg.transform.flip(pg.image.load('resources/images/sprites/heroine/heart.png'), True, False)
        bossHead = pg.image.load('resources/images/sprites/boss/head.png')
        appIcon = pg.image.load('resources/images/app/icon.png')
        mainScreen = pg.image.load('resources/images/world/1.png')
        cursor = pg.image.load('resources/images/app/cursor.png')
        livesImg = pg.transform.scale(pg.image.load('resources/images/sprites/heroine/die/8.png'), (48, 32))

        timerFont = pg.font.Font('resources/fonts/timer.ttf', 30)
        levelFont = pg.font.Font('resources/fonts/font2.ttf', 30)
        checkpointFont = pg.font.Font('resources/fonts/lemonmilk.otf', 20)
        mainMenuFont = pg.font.Font('resources/fonts/font.ttf', 30)
        saveFont = pg.font.Font('resources/fonts/font.ttf', 30)
        saveFont2 = pg.font.Font('resources/fonts/font.ttf', 50)
        nameFont = pg.font.Font('resources/fonts/font.ttf', 42)

        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_icon(appIcon)
        pg.display.set_caption("Zombie Invasion: Apocalypse")
        pg.mouse.set_visible(False)
        clock = pg.time.Clock()
        mainScreen = pg.transform.scale(mainScreen, (1316, 740))

        saveText2 = saveFont2.render("Name", True, (255, 255, 255))
        empty = saveFont2.render("", True, (0, 0, 0))
        nameIn = nameFont.render(nameText, True, (0, 0, 0))

        cursorRect = cursor.get_rect()
        heart_rect = heart.get_rect(center=(5, 0))
        bossHead_rect = bossHead.get_rect(left=900)
        saveRect2 = saveText2.get_rect(center=(658, 240))
        inputBox = pg.Rect(521, 300, 274, 100)
        nameBox = nameIn.get_rect(center=(658, 350))

        zombieEventTimer = pg.time.get_ticks()
        zombieFreqTimer = pg.time.get_ticks()
        dragonEventTimer = pg.time.get_ticks()
        dragonStartTimer = pg.time.get_ticks()
        updateT = pg.time.get_ticks()

        platform_group.add(platform)
        player_group.add(player_obj)

        for i in range(1, 4):
            livesRect = livesImg.get_rect(center=(i * 50, 85))
            livesList.append(livesImg)
            livesListRect.append(livesRect)

        for i in range(0, 28):
            rr = pg.image.load(f'resources/images/app/dir/frame_{i}_delay-0.08s.png')
            rrlist.append(rr)

        while True:
            screen.fill((40, 40, 40))
            screen.blit(mainScreen, (0, 0))
            cursorRect.center = pg.mouse.get_pos()

            random_side2 = random.randrange(0, 2)

            mainMenuText = mainMenuFont.render("Main Menu", True, (0, 0, 0))
            mainMenuRect = mainMenuText.get_rect(center=(1190, 680))

            saveText = saveFont.render("Save Score", True, (0, 0, 0))
            saveRect = saveText.get_rect(center=(1190, 635))

            mainMenuFont = hover(mainMenuRect, 30, "font", "ttf")
            saveFont = hover(saveRect, 30, "font", "ttf")

            for event in pg.event.get():

                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            scoreDict = {'name': nameText, 'score': player_obj.currScore}
                            abspath = pathlib.Path("leaderboard.pickle").absolute()
                            readBoard = open(str(abspath), "rb")
                            tmp = pickle.load(readBoard)
                            tmp.append(scoreDict)
                            dictList = sorted(tmp, key=itemgetter('score'), reverse=True)
                            with open('leaderboard.pickle', 'wb') as file:
                                pickle.dump(dictList, file, protocol=pickle.HIGHEST_PROTOCOL)

                            windowFlag = False
                            window = 1
                            break

                        elif event.key == pg.K_BACKSPACE:
                            nameText = nameText[:-1]
                            backSpaceSFX.play()
                        elif len(nameText) <= 12:
                            nameText += event.unicode
                            typeSFX.play()

                if event.type == pg.MOUSEBUTTONUP and inputBox.collidepoint(event.pos):
                    active = True
                    nameText = ""
                    nameBox.left = 525
                elif event.type == pg.MOUSEBUTTONUP and not inputBox.collidepoint(event.pos) and save:
                    closeSFX.play()
                    active = False
                    save = False
                    nameText = "Name Here"
                    nameBox.center = (658, 350)

                if event.type == pg.MOUSEBUTTONUP and mainMenuRect.collidepoint(event.pos):
                    buttonSFX.play()
                    windowFlag = False
                    window = 1
                    break

                if event.type == pg.MOUSEBUTTONUP and saveRect.collidepoint(event.pos):
                    buttonSFX.play()
                    openSFX.play()
                    save = True

                if event.type == pg.KEYDOWN and alive:
                    if event.key == pg.K_LEFT:
                        isMovingLeft = True
                        isMovingRight = False
                        isIdleLeft = False
                        isIdleRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = False

                    if event.key == pg.K_RIGHT:
                        isMovingLeft = False
                        isMovingRight = True
                        isIdleLeft = False
                        isIdleRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = False

                    if event.key == pg.K_s and not player_obj.isFlipped:
                        isMovingLeft = False
                        isMovingRight = False
                        isIdleLeft = False
                        isIdleRight = False
                        isShootingLeft = True
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = False

                    if event.key == pg.K_s and player_obj.isFlipped:
                        isMovingLeft = False
                        isMovingRight = False
                        isIdleLeft = False
                        isIdleRight = False
                        isShootingLeft = False
                        isShootingRight = True
                        isShootingLeftUp = False
                        isShootingRightUp = False

                    if event.key == pg.K_w and not player_obj.isFlipped:
                        isMovingLeft = False
                        isMovingRight = False
                        isIdleLeft = False
                        isIdleRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = True
                        isShootingRightUp = False

                    if event.key == pg.K_w and player_obj.isFlipped:
                        isMovingLeft = False
                        isMovingRight = False
                        isIdleLeft = False
                        isIdleRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = True

                    if event.key == pg.K_UP:
                        player_obj.jump()

                    if event.key == pg.K_t:
                        player_obj.hp = 0

                if event.type == pg.KEYUP and alive:
                    if event.key == pg.K_LEFT and not isMovingRight and not isShootingLeft and not isShootingLeftUp:
                        isMovingLeft = False
                        isIdleLeft = True
                    if event.key == pg.K_RIGHT and not isMovingLeft and not isShootingRight and not isShootingRightUp:
                        isMovingRight = False
                        isIdleRight = True
                    if event.key == pg.K_s:
                        if isShootingLeft and not isMovingLeft:
                            isShootingLeft = False
                            isIdleLeft = True
                        if isShootingRight and not isMovingRight:
                            isShootingRight = False
                            isIdleRight = True

                    if event.key == pg.K_w:
                        if isShootingLeftUp and not isMovingLeft:
                            isShootingLeftUp = False
                            isIdleLeft = True
                        if isShootingRightUp and not isMovingRight:
                            isShootingRightUp = False
                            isIdleRight = True

            if not windowFlag:
                windowFlag = True
                break

            # dont mind this

            list1 = list(map(''.join, itertools.product(*zip('Sama'.upper(), 'Sama'.lower()))))
            list2 = list(map(''.join, itertools.product(*zip('Zizo'.upper(), 'Zizo'.lower()))))
            list3 = list(map(''.join, itertools.product(*zip('Ibrahim'.upper(), 'Ibrahim'.lower()))))
            list4 = list(map(''.join, itertools.product(*zip('Waleed'.upper(), 'Waleed'.lower()))))
            list5 = list(map(''.join, itertools.product(*zip('Moaz'.upper(), 'Moaz'.lower()))))
            list6 = list(map(''.join, itertools.product(*zip('Farah'.upper(), 'Farah'.lower()))))
            list7 = list(map(''.join, itertools.product(*zip('Abdo'.upper(), 'Abdo'.lower()))))
            list8 = list(map(''.join, itertools.product(*zip('Abdelrahman'.upper(), 'Abdelrahman'.lower()))))
            list9 = list(map(''.join, itertools.product(*zip('Youssef'.upper(), 'Youssef'.lower()))))

            list10 = list1 + list2 + list3 + list4 + list5 + list6 + list7 + list8 + list9

            if save and (nameText in set(list10)):
                rick = rrlist[frameI]
                if pg.time.get_ticks() - updateT >= 60:
                    updateT = pg.time.get_ticks()
                    frameI += 1
                    if frameI >= 27:
                        frameI = 0
                    rickFlag = True
            else:
                rickFlag = False

            shotZombieDict = pg.sprite.groupcollide(zombies_group, bullet_group, False, True)

            if len(shotZombieDict) != 0:

                shotZombie = list(shotZombieDict.keys())[0]
                if not shotZombie.is_boss:
                    if shotZombie.isDying:
                        if not shotZombie.isFlipped:
                            shotZombie.update_action(8)
                        elif shotZombie.isFlipped:
                            shotZombie.update_action(9)
                        shotZombie.rect.bottom = 610

                    shotZombie.hp = 0
                    zombieDieSFX.play()

            shotDragonDict = pg.sprite.groupcollide(dragon_group, bullet_group, False, True)

            if len(shotDragonDict) != 0:

                shotDragon = list(shotDragonDict.keys())[0]

                if shotDragon.isDying:
                    if not shotDragon.isFlipped:
                        shotDragon.update_action(2)
                    elif shotDragon.isFlipped:
                        shotDragon.update_action(3)

                shotDragon.hp = 0
                dragonDieSFX.play()

            if oneLevel:
                if levels <= 3 or levels == 5:
                    level = levels
                    if levels == 5:
                        dragonsWave = True
                if levels == 4:
                    level = 4
                    dragonsWave = True
                if levels == 6:
                    pg.mixer.music.stop()
                    pg.mixer.music.load('resources/sounds/music/boss.wav')
                    pg.mixer.music.play(-1)
                    level = 6
                    dragonsWave = True
                    bossDelay = pg.time.get_ticks()
                mainScreen = pg.image.load(f'resources/images/world/{level}.png')
                mainScreen = pg.transform.scale(mainScreen, (1316, 740))
                oneLevel = False
                noTimer = True
                player_obj = level_up()

            if zero and noTimer:
                alive = False
                zombiesWave = False
                dragonsWave = False
                isMovingLeft = False
                isMovingRight = False
                isShootingLeft = False
                isShootingRight = False
                isShootingLeftUp = False
                isShootingRightUp = False

            if mode == 1:

                if bossExists:
                    if boss_obj.hp <= 1500 and checkpoint:
                        checkpointTimer = pg.time.get_ticks()
                        checkpoint = False
                        checkpointFlag = True
                        checkpointText = checkpointFont.render(f'Checkpoint!', True, (255, 255, 255))
                        checkpointRect = checkpointText.get_rect(center=(1210, 67))

                    if checkpointFlag:
                        if pg.time.get_ticks() - checkpointTimer <= 5000:
                            screen.blit(checkpointText, checkpointRect)

                if player_obj.hp <= 0:
                    if lives == 0:
                        zombiesWave = False
                        dragonsWave = False
                        player_obj.die()
                        text, text_rect, isGameOver = game_over(noTimer, zero)
                        isMovingLeft = False
                        isMovingRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = False
                        loseFlagSFX = False
                        winFlagSFX = False
                    else:
                        lifeLostSFX.play()
                        rtime = 59
                        lives -= 1
                        livesListRect.pop()
                        bullet_group.empty()
                        fireball_group.empty()
                        zombies_group.empty()
                        dragon_group.empty()
                        player_group.empty()
                        if bossExists:
                            if boss_obj.hp > 1500:
                                boss_group.empty()
                                boss_obj = boss.Boss()
                                boss_group.add(boss_obj)
                            else:
                                boss_obj.rect.centerx = 877
                                boss_obj.hp = 1500
                        player_obj = player.Player()
                        player_group.add(player_obj)
                elif level == 6 and bossExists:
                    if boss_obj.hp <= 0:
                        zombiesWave = False
                        dragonsWave = False

                if rtime > 0 and level != 6 and alive:
                    if timeFlag:
                        if datetime.datetime.now().second == 59:
                            now = 0
                        else:
                            now = datetime.datetime.now().second
                        timeFlag = False
                    if abs(datetime.datetime.now().second - now) == 1:
                        timeFlag = True
                        rtime -= 1
                        remaining_mins = int(rtime / 60)
                        remaining_secs = int(rtime % 60)
                if rtime <= 0:
                    zero = True
                if rtime <= 0 and not noTimer:
                    if level == 1:
                        level = 2
                        player_obj = level_up()
                    elif level == 2:
                        level = 3
                        player_obj = level_up()
                    elif level == 3:
                        level = 4
                        player_obj = level_up()
                        dragonsWave = True
                    elif level == 4:
                        level = 5
                        player_obj = level_up()
                    elif level == 5:
                        pg.mixer.music.stop()
                        pg.mixer.music.load('resources/sounds/music/boss.wav')
                        pg.mixer.music.play(-1)
                        level = 6
                        bossDelay = pg.time.get_ticks()
                        player_obj = level_up()
                    mainScreen = pg.image.load(f'resources/images/world/{level}.png')
                    mainScreen = pg.transform.scale(mainScreen, (1316, 740))

                    rtime = 59

                if rtime <= 0 and noTimer:
                    text, text_rect, isGameOver = game_over(noTimer, zero)

                if not bossExists and level == 6 and pg.time.get_ticks() - bossDelay >= 5000:
                    boss_obj = boss.Boss()
                    boss_group.add(boss_obj)
                    bossExists = True

                if level == 6 and bossExists:
                    if boss_obj.hp <= 0:
                        text, text_rect, isGameOver = game_over(noTimer, zero)
                        isMovingLeft = False
                        isMovingRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = False
                        loseFlagSFX = False
                        if winFlag:
                            winDelay = pg.time.get_ticks()
                            isWin = True
                            winFlag = False
                        if winFlagSFX and pg.time.get_ticks() - winDelay >= 2000:
                            winFlagSFX = False
                            winSFX.play()

                if level == 2:
                    zombieFreq = 500
                if level == 3:
                    zombieFreq = 400
                if level == 4:
                    zombieFreq = 550
                    dragonFreq = 6000
                if level == 5:
                    zombieFreq = 500
                    dragonFreq = 4000
                if level == 6:
                    zombieFreq = 3000
                    dragonFreq = 6000

                    if bossExists:
                        if boss_obj.hp <= 0 and boss_obj.isDying:
                            if not boss_obj.isFlipped:
                                boss_obj.update_action(8)
                            elif boss_obj.isFlipped:
                                boss_obj.update_action(9)
                            boss_obj.rect.bottom = 610

                if remaining_secs < 10:
                    timer = timerFont.render(f"{remaining_mins}:0{remaining_secs}", True, (255, 255, 255))
                else:
                    timer = timerFont.render(f"{remaining_mins}:{remaining_secs}", True, (255, 255, 255))

                levelText = levelFont.render(f"Level {level}", True, (255, 255, 255))
                levelRect = levelText.get_rect(center=(1210, 37))
                timerRect = timer.get_rect(center=(1210, 75))
                screen.blit(levelText, levelRect)
                if level != 6:
                    screen.blit(timer, timerRect)

            elif mode == 2:
                fontScore = pg.font.Font('resources/fonts/font.ttf', 20)
                scoreText = fontScore.render(f"Score {player_obj.currScore}", True, (255, 255, 255))
                scoreTextRect = scoreText.get_rect(center=(1200, 40))
                screen.blit(scoreText, scoreTextRect)

                if player_obj.hp > 0:
                    player_obj.currScore += 2
                    if pg.time.get_ticks() - zombieFreqTimer >= 1000 and zombieFreq > 400:
                        zombieFreqTimer = pg.time.get_ticks()
                        zombieFreq -= 5
                else:
                    if lives == 0:
                        zombiesWave = False
                        dragonsWave = False
                        player_obj.die()
                        text, text_rect, isGameOver = game_over(noTimer, zero)
                        isMovingLeft = False
                        isMovingRight = False
                        isShootingLeft = False
                        isShootingRight = False
                        isShootingLeftUp = False
                        isShootingRightUp = False
                        loseFlagSFX = False
                        winFlagSFX = False
                    else:
                        lifeLostSFX.play()
                        rtime = 59
                        lives -= 1
                        livesListRect.pop()
                        bullet_group.empty()
                        fireball_group.empty()
                        zombies_group.empty()
                        dragon_group.empty()
                        player_group.empty()
                        player_obj = player.Player()
                        player_group.add(player_obj)

            if mode == 2 and pg.time.get_ticks() - dragonStartTimer >= 90000:
                dragonsWave = True
                dragonFreq = 3000

            if pg.time.get_ticks() - zombieEventTimer >= zombieFreq and zombiesWave:

                zombieEventTimer = pg.time.get_ticks()

                if mode == 2:
                    if pg.time.get_ticks() - zombieEventTimer >= 60000 and zombieSpeed < 3:
                        zombieEventTimer = pg.time.get_ticks()
                        zombieSpeed += 0.5

                zombie_obj = zombie.Zombie(zombieSpeed, False)
                zombies_group.add(zombie_obj)

            if pg.time.get_ticks() - dragonEventTimer >= dragonFreq and dragonsWave:
                dragonEventTimer = pg.time.get_ticks()
                if random_side2 == 0:
                    random_xpos2 = range(-100, -90)
                    isFlippedDragon = True
                else:
                    random_xpos2 = range(1406, 1416)
                    isFlippedDragon = False

                random_ypos = range(100, 250)

                if level == 4:
                    dragon_obj = dragon.Dragon(random.choice(random_xpos2), random.choice(random_ypos), isFlippedDragon,
                                               "yellow")
                elif level == 5 or level == 6:
                    dragon_obj = dragon.Dragon(random.choice(random_xpos2), random.choice(random_ypos), isFlippedDragon,
                                               "red")
                if mode == 2:
                    randomCol = random.choice(["yellow", "red"])
                    dragon_obj = dragon.Dragon(random.choice(random_xpos2), random.choice(random_ypos), isFlippedDragon,
                                               randomCol)

                dragon_group.add(dragon_obj)

            main_game()
            platform_group.draw(screen)

            x, y = pg.mouse.get_pos()
            if not alive and 0 < x < 1315 and 0 < y < 739:
                screen.blit(cursor, cursorRect)

            if isGameOver:
                if isWin:
                    if pg.time.get_ticks() - winDelay >= 2000:
                        screen.blit(text, text_rect)
                else:
                    screen.blit(text, text_rect)
                if mode == 2:
                    screen.blit(saveText, saveRect)
                    if save:
                        x, y = pg.mouse.get_pos()
                        pg.draw.rect(screen, (0, 0, 0), (458, 200, 400, 250))
                        pg.draw.rect(screen, (255, 255, 255), (521, 300, 274, 100))
                        screen.blit(saveText2, saveRect2)
                        screen.blit(empty, inputBox)
                        nameIn = nameFont.render(nameText, True, (0, 0, 0))
                        screen.blit(nameIn, nameBox)

            if rickFlag:
                screen.blit(rick, (30, 160))
            screen.blit(mainMenuText, mainMenuRect)
            if 0 < x < 1315 and 0 < y < 739:
                screen.blit(cursor, cursorRect)
            print(zombieFreq)
            for rect in livesListRect:
                screen.blit(livesImg, rect)
            pg.display.update()
            clock.tick(60)

    if window == 3:

        appIcon = pg.image.load('resources/images/app/icon.png')
        mainScreen = pg.image.load('resources/images/app/leaderboard.jpg')
        cursor = pg.image.load('resources/images/app/cursor.png')

        mainMenuFont = pg.font.Font('resources/fonts/font.ttf', 30)
        leaderBoardNamesFont = pg.font.Font('resources/fonts/font.ttf', 45)
        mainFont = pg.font.Font('resources/fonts/font.ttf', 90)
        clrFont = pg.font.Font('resources/fonts/font.ttf', 30)

        pg.display.set_caption("Zombie Invasion: Apocalypse")
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_icon(appIcon)
        clock = pg.time.Clock()
        mainScreen = pg.transform.scale(mainScreen, (WIDTH, HEIGHT))

        pg.mouse.set_visible(True)
        cursorRect = cursor.get_rect()
        pg.mouse.set_visible(False)
        MAX_X, MAX_Y = screen.get_size()

        with open("leaderboard.pickle", "rb") as file:
            loadedList = pickle.load(file)

        if len(loadedList) >= 1:
            top1 = leaderBoardNamesFont.render(f"{loadedList[0].get('name')}", True, (255, 255, 255))
            top1Rect = top1.get_rect(top=220)
            top1Rect.left = 358
            top1s = leaderBoardNamesFont.render(f"{loadedList[0].get('score')}", True, (255, 255, 255))
            top1sRect = top1.get_rect(top=220)
            top1sRect.left = 855

        if len(loadedList) >= 2:
            top2 = leaderBoardNamesFont.render(f"{loadedList[1].get('name')}", True, (255, 255, 255))
            top2Rect = top2.get_rect(top=270)
            top2Rect.left = 358
            top2s = leaderBoardNamesFont.render(f"{loadedList[1].get('score')}", True, (255, 255, 255))
            top2sRect = top2.get_rect(top=270)
            top2sRect.left = 855

        if len(loadedList) >= 3:
            top3 = leaderBoardNamesFont.render(f"{loadedList[2].get('name')}", True, (255, 255, 255))
            top3Rect = top3.get_rect(top=320)
            top3Rect.left = 358
            top3s = leaderBoardNamesFont.render(f"{loadedList[2].get('score')}", True, (255, 255, 255))
            top3sRect = top3.get_rect(top=320)
            top3sRect.left = 855

        if len(loadedList) >= 4:
            top4 = leaderBoardNamesFont.render(f"{loadedList[3].get('name')}", True, (255, 255, 255))
            top4Rect = top4.get_rect(top=370)
            top4Rect.left = 358
            top4s = leaderBoardNamesFont.render(f"{loadedList[3].get('score')}", True, (255, 255, 255))
            top4sRect = top4.get_rect(top=370)
            top4sRect.left = 855

        if len(loadedList) >= 5:
            top5 = leaderBoardNamesFont.render(f"{loadedList[4].get('name')}", True, (255, 255, 255))
            top5Rect = top5.get_rect(top=420)
            top5Rect.left = 358
            top5s = leaderBoardNamesFont.render(f"{loadedList[4].get('score')}", True, (255, 255, 255))
            top5sRect = top5.get_rect(top=420)
            top5sRect.left = 855

        while True:
            screen.blit(mainScreen, (0, 0))
            cursorRect.center = pg.mouse.get_pos()

            leaderBoardTitle = mainFont.render("Leaderboard", True, (255, 255, 255))
            mainMenuText2 = mainMenuFont.render("Main Menu", True, (255, 255, 255))
            clrText = clrFont.render("Clear leaderboard", True, (255, 255, 255))

            leaderBoardTitleRect = leaderBoardTitle.get_rect(center=(WIDTH / 2, 100))
            mainMenuRect2 = mainMenuText2.get_rect(center=(1190, 670))
            clrRect = clrText.get_rect(center=(170, 670))

            mainMenuFont = hover(mainMenuRect2, 30, "font", "ttf")
            clrFont = hover(clrRect, 30, "font", "ttf")

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONUP and mainMenuRect2.collidepoint(event.pos):
                    buttonSFX.play()
                    windowFlag = False
                    window = 1
                    mainSFXFlag = True
                    break

                if event.type == pg.MOUSEBUTTONUP and clrRect.collidepoint(event.pos):
                    buttonSFX.play()
                    dictList = []
                    with open('leaderboard.pickle', 'wb') as file:
                        pickle.dump(dictList, file, protocol=pickle.HIGHEST_PROTOCOL)

                    windowFlag = False
                    window = 3
                    break

            if not windowFlag:
                windowFlag = True
                break

            if len(loadedList) >= 1:
                screen.blit(top1, top1Rect)
                screen.blit(top1s, top1sRect)
            if len(loadedList) >= 2:
                screen.blit(top2, top2Rect)
                screen.blit(top2s, top2sRect)
            if len(loadedList) >= 3:
                screen.blit(top3, top3Rect)
                screen.blit(top3s, top3sRect)
            if len(loadedList) >= 4:
                screen.blit(top4, top4Rect)
                screen.blit(top4s, top4sRect)
            if len(loadedList) >= 5:
                screen.blit(top5, top5Rect)
                screen.blit(top5s, top5sRect)

            screen.blit(mainMenuText2, mainMenuRect2)
            screen.blit(leaderBoardTitle, leaderBoardTitleRect)
            screen.blit(clrText, clrRect)

            x, y = pg.mouse.get_pos()
            if 0 < x < MAX_X - 1 and 0 < y < MAX_Y - 1:
                screen.blit(cursor, cursorRect)
            pg.display.update()
            clock.tick(60)
