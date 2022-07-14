import datetime
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

lives = 3
level = 1
remaining_mins = 1
remaining_secs = 30
rtime = 90

zombiesWave = True
dragonsWave = False
isGameOver = False
bossExists = False

checkpoint = True
checkpointFlag = False

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

screen = pg.display.set_mode((WIDTH,HEIGHT))

heart = pg.transform.flip(pg.image.load('resources/images/sprites/heroine/heart.png'),True,False)
heart_rect = heart.get_rect(center = (5,0))

bossHead = pg.image.load('resources/images/sprites/boss/head.png')
bossHead_rect = bossHead.get_rect(left = 900)

appIcon = pg.image.load('resources/images/app/icon.png')
pg.display.set_icon(appIcon)
pg.display.set_caption("Zombie Invasion: Apocalypse")
clock = pg.time.Clock()
pg.mouse.set_visible(False)
mainScreen = pg.image.load('resources/images/world/level1/1.png')
mainScreen = pg.transform.scale(mainScreen,(1316,740))
cursor = pg.image.load('resources/images/app/cursor.png')
cursorRect = cursor.get_rect()

timerFont = pg.font.Font('resources/fonts/timer.ttf',30)
levelFont = pg.font.Font('resources/fonts/lemonmilk.otf',30)
checkpointFont = pg.font.Font('resources/fonts/lemonmilk.otf',20)

livesList = []
livesListRect = []
livesImg = pg.transform.scale(pg.image.load('resources/images/sprites/heroine/die/8.png'), (48,32))
for i in range(1,4):
    livesRect = livesImg.get_rect(center = ((i * 50, 85)))
    livesList.append(livesImg)
    livesListRect.append(livesRect)


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
    zombieSpeed = 2
elif mode == 2:
    zombieFreq = 800
    zombieSpeed = 1

dragonFreq = 3000

zombieEventTimer = pg.time.get_ticks()
zombieFreqTimer = pg.time.get_ticks()

dragonEventTimer = pg.time.get_ticks()
dragonStartTimer = pg.time.get_ticks()

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
    player_group.add(player)
    return player

def game_over():
    bullet_group.empty()
    fireball_group.empty()
    cursorRect.center = pg.mouse.get_pos()
    gameOverFont = pg.font.Font('resources/fonts/game_over.ttf',180)

    if lives == 0:
        text = gameOverFont.render("Game Over",True,(255,255,255))
        text_rect = text.get_rect(center = (653,243))
        isGameOver = True
    if bossExists:
        if boss.hp <= 0:
            gameOverFont = pg.font.Font('resources/fonts/game_over.ttf',180)
            text = gameOverFont.render("You Won",True,(255,255,255))
            text_rect = text.get_rect(center = (653,243))
            isGameOver = True
        
    

    return text, text_rect, isGameOver

def main_game():
    
    pg.draw.rect(screen,(255,255,255),(58,35,200,10))
    pg.draw.rect(screen,(191,33,48),(58,35,player_group.sprite.hp,10))
    screen.blit(heart,(0,2))

    if bossExists:
        if level == 6 and boss.hp > 0:
            pg.draw.rect(screen,(105,105,105),(405,32,506,26))
            pg.draw.rect(screen, (34,139,34),(408,35,boss_group.sprite.hp/4,20))
            pg.draw.rect(screen,(105,105,105),(658,35,6,20))
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

    if bossExists:
        if level == 6:
            if boss.rect.centerx >= WIDTH:
                boss.rect.centerx = 0
            if boss.rect.centerx < 0:
                boss.rect.centerx = WIDTH

timeFlag = True

while True:
    screen.fill((0,0,0))
    screen.blit(mainScreen,(0,0))
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
        
        shotZombie = list(shotZombieDict.keys())[0]
        if not shotZombie.isBoss:
            if shotZombie.isDying:
                if not shotZombie.isFlipped:
                    shotZombie.update_action(8)
                elif shotZombie.isFlipped:
                    shotZombie.update_action(9)
                shotZombie.rect.bottom = 555

            shotZombie.hp = 0

    shotDragonDict = pg.sprite.groupcollide(dragon_group, bullet_group, False, True)
    
    if len(shotDragonDict) != 0:
        
        shotDragon = list(shotDragonDict.keys())[0]
        
        if shotDragon.isDying: # check this line
            if not shotDragon.isFlipped:
                shotDragon.update_action(2)
            elif shotDragon.isFlipped:
                shotDragon.update_action(3)

        shotDragon.hp = 0

    if mode == 1:

        if bossExists:
            if boss.hp <= 50 and checkpoint:
                checkpointTimer = pg.time.get_ticks()
                checkpoint = False
                checkpointFlag = True
                checkpointText = checkpointFont.render(f'Checkpoint!',True,(255,255,255))
                checkpointRect = checkpointText.get_rect(center = (1210, 67))
            
            if checkpointFlag:
                if pg.time.get_ticks() - checkpointTimer <= 5000:
                    screen.blit(checkpointText, checkpointRect)

        if player_group.sprite.hp <= 0:
            if lives == 0:
                zombiesWave = False
                dragonsWave = False
                player.die()
                text, text_rect, isGameOver = game_over()
            else:
                lives -= 1
                livesListRect.pop()
                rtime = 90
                bullet_group.empty()
                fireball_group.empty()
                zombies_group.empty()
                dragon_group.empty()
                player_group.empty()
                if bossExists:
                    if boss.hp > 1000:
                        boss_group.empty()
                        boss = Boss.Boss()
                        boss_group.add(boss)
                    else:
                        boss.rect.centerx = 877
                player = pl.Player()
                player_group.add(player)
        elif level == 6 and bossExists:
            if boss.hp <= 0:
                zombiesWave = False
                dragonsWave = False



        if rtime > 0 and level !=  6 and alive:
            if timeFlag:
                if datetime.datetime.now().second == 59:
                    now = 0
                else:
                    now = datetime.datetime.now().second
                timeFlag = False
            if (abs(datetime.datetime.now().second - now) == 1):
                timeFlag = True
                rtime -= 1
                remaining_mins = int(rtime/60)
                remaining_secs = int(rtime%60)
            print(datetime.datetime.now().second, now, datetime.datetime.now().second - now)
        
        if rtime <= 0:
            if level == 1:
                level = 2
                player = levelUp()
            elif level == 2:
                level = 3
                player = levelUp()
            elif level == 3:
                level = 4
                player = levelUp()
                dragonsWave = True
            elif level == 4:
                level = 5
                player = levelUp()
            elif level == 5:
                level = 6
                bossDelay = pg.time.get_ticks()
                player = levelUp()
            
            rtime = 90

        if not bossExists and level == 6 and pg.time.get_ticks() - bossDelay >= 5000:
            boss = Boss.Boss()
            boss_group.add(boss)
            bossExists = True

        if level == 6 and bossExists:
            if boss.hp <= 0:
                text, text_rect, isGameOver = game_over()

        if level == 2:
            zombieFreq = 500
        if level == 3:
            zombieFreq = 400
        if level == 4:
            zombieFreq = 500
            dragonFreq = 3000
        if level == 5:
            zombieFreq = 400
            dragonFreq = 2000
        if level == 6:
            zombieFreq = 3000
            dragonFreq = 5000
                
            if bossExists:
                if boss.hp <= 0 and boss.isDying:
                    if not boss.isFlipped:
                        boss.update_action(8)
                    elif boss.isFlipped:
                        boss.update_action(9)
                    boss.rect.bottom = 555

        if remaining_secs < 10:
            timer = timerFont.render(f"{remaining_mins}:0{remaining_secs}",True,(255,255,255))
        else:
            timer = timerFont.render(f"{remaining_mins}:{remaining_secs}",True,(255,255,255))
        
        levelText = levelFont.render(f"Level {level}",True,(255,255,255))
        levelRect = levelText.get_rect(center = (1210, 37))
        timerRect = timer.get_rect(center = (1210, 75))
        screen.blit(levelText, levelRect)
        if level != 6:
            screen.blit(timer,timerRect)

        mainScreen = pg.image.load(f'resources/images/world/level{level}/{level}.png')
        mainScreen = pg.transform.scale(mainScreen,(1316,740))
        
    elif mode == 2:
        fontScore = pg.font.Font('resources/fonts/font.ttf',20)
        scoreText = fontScore.render(f"Score {player.currScore}",True,(255,255,255))
        scoreTextRect = scoreText.get_rect(center = (1200,40))
        screen.blit(scoreText,scoreTextRect)
        
        if player_group.sprite.hp > 0:
            player.currScore += 2
            if pg.time.get_ticks() - zombieFreqTimer >= 1000 and zombieFreq > 400:
                zombieFreqTimer = pg.time.get_ticks()
                zombieFreq -= 5
        else:
            zombiesWave = False
            dragonsWave = False
            if lives == 0:
                player.die()
                text, text_rect, isGameOver = game_over()
            else:
                lives -= 1
                livesListRect.pop()
                rtime = 90
                bullet_group.empty()
                fireball_group.empty()
                zombies_group.empty()
                dragon_group.empty()
                player_group.empty()
                player = pl.Player()
                player_group.add(player)
    
    if mode == 2 and pg.time.get_ticks() - dragonStartTimer >= 90000:
        dragonsWave = True
        dragonFreq = 3000


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
        if mode == 2:
            randomCol = random.choice(["yellow","red"])
            dragon = dr.Dragon(random.choice(random_xpos2),random.choice(random_ypos),isFlippedDragon, randomCol)

        dragon_group.add(dragon)

    main_game()
    platform_group.draw(screen)
    x, y = pg.mouse.get_pos()
    if not alive and x > 0 and x < 1315 and y > 0 and y < 739: #boss   
        screen.blit(cursor, cursorRect)

    if bossExists:
        print(boss.rect.left,boss.rect.right)
    if isGameOver:
        screen.blit(text,text_rect)
    
    for rect in livesListRect:
        screen.blit(livesImg, rect)

    pg.display.update()
    clock.tick(60)