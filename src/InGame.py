import pygame as pg, math, random, sys
from sprites import Player as pl
from sprites import Platform as pt
from sprites import Zombie as zm
from pygame import mixer 
pg.init()

WIDTH = 1316
HEIGHT = 740

alive = True
isIdleLeft = True
isIdleRight = False
isMovingLeft = False
isMovingRight = False
isIdleLeft = False
isIdleRight = False
isShootingLeft = False
isShootingRight = False
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
pg.mouse.set_visible(True)
mainScreen = pg.image.load('resources/images/world/level1/1.png')
mainScreen = pg.transform.scale(mainScreen,(1316,740))


player = pl.Player()
player_group = pg.sprite.GroupSingle()
player_group.add(player)

zombies_group = pg.sprite.Group()
hostile_event = pg.USEREVENT
pg.time.set_timer(hostile_event,600)

platform = pt.Platform()
platform_group = pg.sprite.GroupSingle()
platform_group.add(platform)

bullet_group = pg.sprite.Group()

def game_over():
    gameOverFont = pg.font.Font('resources/fonts/game_over.ttf',180)
    text = gameOverFont.render("Game Over",True,(255,255,255))
    text_rect = text.get_rect(center = (653,243))
    screen.blit(text,text_rect)



def main_game():
    
    pg.draw.rect(screen,(255,255,255),(58,35,200,10))
    pg.draw.rect(screen,(191,33,48),(58,35,2 * player_group.sprite.hp,10))
    

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


    # if pygame.sprite.spritecollide(player_group.sprite,hostiles_group,True):
    #     player_group.sprite.get_damage(10)

    #     zombie_die = mixer.Sound('Zombie.wav')
    #     zombie_die.play()
        

while True:
    screen.fill((0,0,0))
    screen.blit(mainScreen,(0,0))
    screen.blit(heart,(0,2))

    random_side = random.randrange(0,2)
    for event in pg.event.get():

        if event.type == hostile_event:
            if random_side == 0: 
                random_xpos = range(-20,180)
                isFlippedZombie = True
            else:
                random_xpos = range(1136,1336)
                isFlippedZombie = False
                
            random_speed = [2]
            zombie = zm.Zombie(random.choice(random_xpos),555,random.choice(random_speed),isFlippedZombie)
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
            if event.key == pg.K_LEFT:
                isMovingLeft = False
                isIdleLeft = True
            if event.key == pg.K_RIGHT:
                isMovingRight = False
                isIdleRight = True
            if event.key == pg.K_s:
                if isShootingLeft:
                    isShootingLeft = False
                    isIdleLeft = True
                if isShootingRight:
                    isShootingRight = False
                    isIdleRight = True
    
    shotZombieDict = pg.sprite.groupcollide(zombies_group, bullet_group, False, True)
    
    if len(shotZombieDict) != 0:
        
        shotZombie = list(shotZombieDict.keys())[0]
        
        if shotZombie.isDying:
            if not shotZombie.isFlipped:
                shotZombie.update_action(8)
            elif shotZombie.isFlipped:
                shotZombie.update_action(9)

        shotZombie.hp = 0

    main_game()

    if player_group.sprite.hp > 0:
        pass
    else:
        pg.time.set_timer(hostile_event,0)
        player.die()
        game_over()

    pg.display.update()
    platform_group.draw(screen)
    clock.tick(60)