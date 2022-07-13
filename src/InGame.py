from sprites import Player as pl
from sprites import Platform as pt
from sprites import Zombie as zm
from sprites import Dragon as dr
from sprites import Boss 
from pygame import mixer
import pygame as pg, random, sys, pickle, pathlib
pg.init()

WIDTH = 1316
HEIGHT = 740

currScore = 0
level = 3
lives = 3
zombiesWave = True
dragonsWave = False

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

isFlyingLeft = False
isFlyingRight = False
isDyingLeft = False
isDyingRight = False



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

dragon_group = pg.sprite.Group()
dragonEvent = pg.USEREVENT

boss_group = pg.sprite.GroupSingle()

if mode == 1:
    zombieFreq = 600
    dragonFreq = 600
    zombieSpeed = 2
elif mode == 2:
    zombieFreq = 800
    dragonFreq = 600
    zombieSpeed = 1

zombiesShot = 0
zombieEventTimer = pg.time.get_ticks()

dragonsShot = 0
dragonEventTimer = pg.time.get_ticks()

platform = pt.Platform()
platform_group = pg.sprite.GroupSingle()
platform_group.add(platform)

bullet_group = pg.sprite.Group()
fireball_group = pg.sprite.Group()

player = pl.Player()
player_group = pg.sprite.GroupSingle()
player_group.add(player)

def levelUp():
    bullet_group.empty()
    fireball_group.empty()
    zombies_group.empty()
    dragon_group.empty()
    player_group.empty()
    player = pl.Player()
    print(player.action)
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
        player.update_action(0)
    if isIdleRight:
        player.update_action(1)
    if isMovingLeft:
        player.update_action(2)
    if isMovingRight:
        player.update_action(3)
    if isShootingLeft or isShootingLeftUp:
        player.update_action(4)
    if isShootingRight or isShootingRightUp:
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
            player.shoot(False)
            player.shootingCoolDown = 10

    if isShootingLeftUp or isShootingRightUp:
        if player.shootingCoolDownUp == 0:
            # Fireball_sound = mixer.Sound('Fireball.wav')
            # Fireball_sound.play()
            player.shoot(True)
            player.shootingCoolDownUp = 10

    if player.pos.x > WIDTH:
        player.pos.x = 0
    if player.pos.x < 0:
        player.pos.x = WIDTH

while True:
    screen.fill((0,0,0))
    screen.blit(mainScreen,(0,0))
    screen.blit(heart,(0,2))
    random_side2 = random.randrange(0,2)
    
    for event in pg.event.get():
        
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

            if event.key == pg.K_s and not player.isFlipped:
                isMovingLeft = False
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = True
                isShootingRight = False
                isShootingLeftUp = False
                isShootingRightUp = False

            if event.key == pg.K_s and player.isFlipped:
                isMovingLeft = False
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = False
                isShootingRight = True
                isShootingLeftUp = False
                isShootingRightUp = False

            if event.key == pg.K_w and not player.isFlipped:
                isMovingLeft = False
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = False
                isShootingRight = False
                isShootingLeftUp = True
                isShootingRightUp = False

            if event.key == pg.K_w and player.isFlipped:
                isMovingLeft = False
                isMovingRight = False
                isIdleLeft = False
                isIdleRight = False
                isShootingLeft = False
                isShootingRight = False
                isShootingLeftUp = False
                isShootingRightUp = True
            
            if event.key == pg.K_UP:
                player_group.sprite.jump()

            if event.key == pg.K_t:
                player.hp = 0

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

    shotDragonDict = pg.sprite.groupcollide(dragon_group, bullet_group, False, True)
    
    if len(shotDragonDict) != 0:
        if mode == 1:
            dragonsShot += 1
        
        shotDragon = list(shotDragonDict.keys())[0]
        
        if shotDragon.isDying: # check this line
            if not shotDragon.isFlipped:
                shotDragon.update_action(2)
            elif shotDragon.isFlipped:
                shotDragon.update_action(3)

        shotDragon.hp = 0

    if mode == 1:
        if player_group.sprite.hp <= 0:
            zombiesWave = False
            dragonsWave = False
            player.die()
            game_over()

        if level == 1 and zombiesShot == 1:
            player = levelUp()
            level = 2
            zombiesShot = 0
        if level == 2 and zombiesShot == 1:
            player = levelUp()
            level = 3
            zombiesShot = 0
        if level == 3 and zombiesShot == 1:
            player = levelUp()
            level = 4
            dragonsWave = True
            zombiesShot = 0
        if level == 4 and zombiesShot == 1:
            player = levelUp()
            level = 5
            zombiesShot = 0
        if level == 5 and zombiesShot == 1:
            player = levelUp()
            level = 6
            zombiesShot = 0
            zombiesWave = False #
            boss = Boss.Boss()
            boss_group.add(boss)
        if level == 6 and boss.hp == 0:
            game_over()

        if level == 2:
            zombieFreq = 600
        if level == 3:
            zombieFreq = 500
        if level == 4:
            zombieFreq = 500
            dragonFreq = 3000
        if level == 5:
            zombieFreq = 400
            dragonFreq = 2000
        if level == 6:
            zombieFreq = 8000
            dragonFreq = 3000 #11000

        mainScreen = pg.image.load(f'resources/images/world/level{level}/{level}.png')
        mainScreen = pg.transform.scale(mainScreen,(1316,740))
        
    elif mode == 2:
        fontScore = pg.font.Font('resources/fonts/font.ttf',20)
        scoreText = fontScore.render(f"Score {currScore}",True,(255,255,255))
        scoreTextRect = scoreText.get_rect(center = (1200,40))
        screen.blit(scoreText,scoreTextRect)
        
        if player_group.sprite.hp > 0:
            currScore += 2
            if pg.time.get_ticks() - zombieEventTimer >= 1000 and zombieFreq > 300:
                zombieEventTimer = pg.time.get_ticks()
                zombieFreq -= 5
        else:
            zombiesWave = False
            dragonsWave = False
            player.die()
            game_over()
    


    if pg.time.get_ticks() - zombieEventTimer >= zombieFreq and zombiesWave:

        zombieEventTimer = pg.time.get_ticks()
        

        if mode == 2:
            if pg.time.get_ticks() - zombieEventTimer >= 60000 and zombieSpeed < 3:
                zombieEventTimer = pg.time.get_ticks()
                zombieSpeed += 0.5

        zombie = zm.Zombie(zombieSpeed, False)
        zombies_group.add(zombie)

    if pg.time.get_ticks() - dragonEventTimer >= dragonFreq and dragonsWave:
        dragonEventTimer = pg.time.get_ticks()
        if random_side2 == 0: 
            random_xpos2 = range(-100,-90)
            isFlippedDragon = True
        else:
            random_xpos2 = range(1406,1416)
            isFlippedDragon = False

        random_ypos = range(100,200)

        if level == 4:
            dragon = dr.Dragon(random.choice(random_xpos2),random.choice(random_ypos),isFlippedDragon, "yellow")
        elif level == 5 or level == 6:
            dragon = dr.Dragon(random.choice(random_xpos2),random.choice(random_ypos),isFlippedDragon, "red")

        dragon_group.add(dragon)

    main_game()
    platform_group.draw(screen)
    x, y = pg.mouse.get_pos()
    if not alive and x > 0 and x < 1315 and y > 0 and y < 739: #boss   
        screen.blit(cursor, cursorRect)
    pg.display.update()
    clock.tick(60)