from sprites import Player as pl
from sprites import Platform as pt
from sprites import Zombie as zm
from pygame import mixer
import pygame as pg, random, sys, pickle, pathlib
pg.init()

WIDTH = 1316
HEIGHT = 740
currScore = 0
level = 1
lives = 3

alive = True
isIdleLeft = True
isIdleRight = False
isMovingLeft = False
isMovingRight = False
isIdleLeft = False
isIdleRight = False
isShootingLeft = False
isShootingRight = False
isShootingLeftUp = False
isShootingRightUp = False

isDeadLeft = False
isDeadRight = False

isIdleLeftZombie = False
isIdleRightZombie = False
isMovingLeftZombie = False
isMovingRightZombie = False
isAttackingLeftZombie = False
isAttackingRightZombie = False
isAppearingLeftZombie = False
isAppearingRightZombie = False
isDeadLeftZombie = False
isDeadRightZombie = False

screen = pg.display.set_mode((WIDTH,HEIGHT))
heart = pg.transform.flip(pg.image.load('resources/images/sprites/heroine/heart.png'),True,False)
heart_rect = heart.get_rect(center = (5,0))
appIcon = pg.image.load('resources/images/app/icon.png')
pg.display.set_icon(appIcon)
pg.display.set_caption("Zombie Invasion: Apocalypse")
clock = pg.time.Clock()
pg.mouse.set_visible(False)
mainScreen = pg.image.load('resources/images/world/level1/1.png')
mainScreen = pg.transform.scale(mainScreen,(1316,740))
cursor = pg.image.load('resources/images/app/cursor.png')
cursorRect = cursor.get_rect()

abspath = pathlib.Path("mode.pickle").absolute()
readMode = open(str(abspath), "rb")
mode = pickle.load(readMode)



zombies_group = pg.sprite.Group()
zombieEvent = pg.USEREVENT

zombieFreq = 100000
zombieSpeed = 1
zombiesShot = 0
pg.time.set_timer(zombieEvent,zombieFreq)
zombieEventTimer = pg.time.get_ticks()

platform = pt.Platform()
platform_group = pg.sprite.GroupSingle()
platform_group.add(platform)

bullet_group = pg.sprite.Group()

player = pl.Player()
player_group = pg.sprite.GroupSingle()
player_group.add(player)

def levelUp():
    bullet_group.empty()
    zombies_group.empty()
    player_group.empty()
    player = pl.Player()
    player_group.add(player)
    return player

def game_over():
    cursorRect.center = pg.mouse.get_pos()

    if player.hp <= 0:
        gameOverFont = pg.font.Font('resources/fonts/game_over.ttf',180)
        text = gameOverFont.render("Game Over",True,(255,255,255))
        text_rect = text.get_rect(center = (653,243))
        screen.blit(text,text_rect)
        currScore = 0
    else:
        gameOverFont = pg.font.Font('resources/fonts/game_over.ttf',180)
        text = gameOverFont.render("You Won",True,(255,255,255))
        text_rect = text.get_rect(center = (653,243))
        screen.blit(text,text_rect)
        currScore = 0


def main_game():
    
    pg.draw.rect(screen,(255,255,255),(58,35,200,10))
    pg.draw.rect(screen,(191,33,48),(58,35,player_group.sprite.hp,10))
    

    bullet_group.draw(screen)  
    player.draw() 
    zombies_group.draw(screen)
    platform_group.draw(screen)

    bullet_group.update()
    zombies_group.update()
    player_group.update()

    if isIdleLeft:
        player.update_action(0)
    if isIdleRight:
        player.update_action(1)
    if isMovingLeft:
        player.update_action(2)
    if isMovingRight:
        player.update_action(3)
    if isShootingLeft:
        player.update_action(4)
    if isShootingRight:
        player.update_action(5)
    if isDeadLeft:
        player.update_action(6)
    if isDeadRight:
        player.update_action(7)

    player.move()

    if isShootingLeft or isShootingRight:
        if player.shootingCoolDown == 0:
            # Fireball_sound = mixer.Sound('Fireball.wav')
            # Fireball_sound.play()
            player.shoot()
            player.shootingCoolDown = 25

    if player.pos.x > WIDTH:
        player.pos.x = 0
    if player.pos.x < 0:
        player.pos.x = WIDTH

while True:
    screen.fill((0,0,0))
    screen.blit(mainScreen,(0,0))
    screen.blit(heart,(0,2))

    random_side = random.randrange(0,2)
    for event in pg.event.get():

        if event.type == zombieEvent:
            if random_side == 0: 
                random_xpos = range(-20,180)
                isFlippedZombie = True
            else:
                random_xpos = range(1136,1336)
                isFlippedZombie = False
                

            if mode == 2:
                if pg.time.get_ticks() - zombieEventTimer >= 60000 and zombieSpeed < 3:
                    zombieEventTimer = pg.time.get_ticks()
                    zombieSpeed += 0.5

            else:
                zombieSpeed = 2

            zombie = zm.Zombie(random.choice(random_xpos),zombieSpeed,isFlippedZombie)
            zombies_group.add(zombie)

        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN and alive:
            if event.key == pg.K_LEFT:
                isMovingLeft = True
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = False
                isShootingRight = False
            if event.key == pg.K_RIGHT:
                isMovingLeft = False
                isMovingRight = True
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = False
                isShootingRight = False
            if event.key == pg.K_s and not player.isFlipped:
                isMovingLeft = False
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = True
                isShootingRight = False
            if event.key == pg.K_s and player.isFlipped:
                isMovingLeft = False
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = False
                isShootingRight = True

            if event.key == pg.K_UP:
                player_group.sprite.jump()

            if event.key == pg.K_t:
                player.hp = 0

        if event.type == pg.KEYUP and alive:
            if event.key == pg.K_LEFT and not isMovingRight and not isShootingLeft:
                isMovingLeft = False
                isIdleLeft = True
            if event.key == pg.K_RIGHT and not isMovingLeft and not isShootingRight:
                isMovingRight = False
                isIdleRight = True
            if event.key == pg.K_s:
                if isShootingLeft and not isMovingLeft:
                    isShootingLeft = False
                    isIdleLeft = True
                if isShootingRight and not isMovingRight:
                    isShootingRight = False
                    isIdleRight = True

    shotZombieDict = pg.sprite.groupcollide(zombies_group, bullet_group, False, True)
    
    if len(shotZombieDict) != 0:
        if mode == 1:
            zombiesShot += 1
        
        shotZombie = list(shotZombieDict.keys())[0]
        
        if shotZombie.isDying:
            if not shotZombie.isFlipped:
                shotZombie.update_action(8)
            elif shotZombie.isFlipped:
                shotZombie.update_action(9)

        shotZombie.hp = 0

    if mode == 1:
        if player_group.sprite.hp <= 0:
            pg.time.set_timer(zombieEvent,0)
            player.die()
            game_over()

        if level == 1 and zombiesShot == 10:
            player = levelUp()
            level = 2
            zombiesShot = 0
        if level == 2 and zombiesShot == 10:
            player = levelUp()
            level = 3
            zombiesShot = 0
        if level == 3 and zombiesShot == 10:
            player = levelUp()
            level = 4
            zombiesShot = 0
        if level == 4 and zombiesShot == 10:
            player = levelUp()
            level = 5
            zombiesShot = 0
        if level == 5 and zombiesShot == 10:
            player = levelUp()
            level = 6
            zombiesShot = 0
        # if level == 6 and boss.hp == 0:
        #     player = levelUp()
        #     game_over()



        mainScreen = pg.image.load(f'resources/images/world/level{level}/{level}.png')
        mainScreen = pg.transform.scale(mainScreen,(1316,740))
        
    else:
        fontScore = pg.font.Font('resources/fonts/font.ttf',20)
        scoreText = fontScore.render(f"Score {currScore}",True,(255,255,255))
        scoreTextRect = scoreText.get_rect(center = (1200,40))
        screen.blit(scoreText,scoreTextRect)
        
        if player_group.sprite.hp > 0:
            currScore += 2
            if pg.time.get_ticks() - zombieEventTimer >= 1000 and zombieFreq > 300:
                zombieEventTimer = pg.time.get_ticks()
                zombieFreq -= 5
                pg.time.set_timer(zombieEvent, zombieFreq)
        else:
            pg.time.set_timer(zombieEvent,0)
            player.die()
            game_over()
    
    main_game()
    platform_group.draw(screen)
    screen.blit(cursor, cursorRect)
    pg.display.update()
    clock.tick(60)