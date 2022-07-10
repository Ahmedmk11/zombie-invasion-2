import pygame as pg, math, random, sys
from sprites import Player as pl
from sprites import Platform as pt
from pygame import mixer 
pg.init()

WIDTH = 1316
HEIGHT = 740
isIdleLeft = True
isIdleRight = False
movingLeft = False
movingRight = False
isIdleLeft = False
isIdleRight = False
isShootingLeft = False
isShootingRight = False
isDeadLeft = False
isDeadRight = False

screen = pg.display.set_mode((WIDTH,HEIGHT))
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

platform = pt.Platform()
platform_group = pg.sprite.GroupSingle()
platform_group.add(platform)

bullet_group = pg.sprite.Group()


def main_game():
    
    pg.draw.rect(screen,(255,0,0),(22,20,200,10))
    pg.draw.rect(screen,(255,0,0),(22,20,2 * player_group.sprite.hp,10))
    # screen.blit(heart,(0,2))

    bullet_group.draw(screen)  
    player.draw() 
    # hostiles_group.draw(screen)
    platform_group.draw(screen)

    bullet_group.update()
    # hostiles_group.update()
    player_group.update()

    # player.screen_edge()

    if isShootingLeft or isShootingRight:
        if player.shootingCoolDown == 0:
            # Fireball_sound = mixer.Sound('Fireball.wav')
            # Fireball_sound.play()
            player.shoot()
            player.shootingCoolDown = 37



    if isIdleLeft:
        player.update_action(0)
    if isIdleRight:
        player.update_action(1)
    if movingLeft:
        player.update_action(2)
    if movingRight:
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



    if player.pos.x > WIDTH:
        player.pos.x = 0
    if player.pos.x < 0:
        player.pos.x = WIDTH


    # if pygame.sprite.spritecollide(player_group.sprite,hostiles_group,True):
    #     player_group.sprite.get_damage(10)



    # if pygame.sprite.groupcollide(hostiles_group, bullet_group,True,True):
    #     zombie_die = mixer.Sound('Zombie.wav')
    #     zombie_die.play()



while True:
    screen.fill((0,0,0))
    screen.blit(mainScreen,(0,0))


    for event in pg.event.get():

        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                movingLeft = True
                isIdleLeft = False
                isIdleRight = False
            if event.key == pg.K_RIGHT:
                movingRight = True
                isIdleLeft = False
                isIdleRight = False
            if event.key == pg.K_SPACE and not player.isFlipped:
                isShootingLeft = True
            if event.key == pg.K_SPACE and player.isFlipped:
                isShootingRight = True

            if event.key == pg.K_UP:
                    player_group.sprite.jump()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                movingLeft = False
                isIdleLeft = True
            if event.key == pg.K_RIGHT:
                movingRight = False
                isIdleRight = True
            if event.key == pg.K_SPACE:
                isShootingLeft = False
                isShootingRight = False



    if player_group.sprite.hp > 0:
        main_game()
    

    pg.display.update()
    platform_group.draw(screen)
    clock.tick(60)