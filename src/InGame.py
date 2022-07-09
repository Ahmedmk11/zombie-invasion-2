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


player = pl.Player(screen)
player_group = pg.sprite.GroupSingle()
player_group.add(player)

platform = pt.Platform()
platform_group = pg.sprite.GroupSingle()
platform_group.add(platform)


def main_game():
    
    pg.draw.rect(screen,(255,0,0),(22,20,200,10))
    pg.draw.rect(screen,(255,0,0),(22,20,2 * player_group.sprite.hp,10))
    # screen.blit(heart,(0,2))

    # bullet_group.draw(screen)  
    player.draw() 
    # hostiles_group.draw(screen)
    platform_group.draw(screen)

    # bullet_group.update()
    # hostiles_group.update()
    player_group.update()

    # player.screen_edge()
    
    # if shoot:
    #     if player.shoot_cooldown == 0:
    #         Fireball_sound = mixer.Sound('Fireball.wav')
    #         Fireball_sound.play()
    #         bullet = Bullets(player.rect.centerx - (0.5 * player.direction * player.rect.size[0]),player.rect.centery - 7,player.direction)
    #         bullet_group.add(bullet)
    #         player.shoot_cooldown = 37




    if isIdleLeft:
        player.update_action(0)
    elif isIdleRight:
        player.update_action(1)
    elif movingLeft:
        player.update_action(2)
    elif movingRight:
        player.update_action(3)
    elif isShootingLeft:
        player.update_action(4)
    elif isShootingRight:
        player.update_action(5)
    elif isDeadLeft:
        player.update_action(6)
    elif isDeadRight:
        player.update_action(7)



    player.move(movingLeft,movingRight)


    # if pygame.sprite.spritecollide(player_group.sprite,hostiles_group,True):
    #     player_group.sprite.get_damage(10)



    # if pygame.sprite.groupcollide(hostiles_group, bullet_group,True,True):
    #     zombie_die = mixer.Sound('Zombie.wav')
    #     zombie_die.play()



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            mixer.music.stop()
            break

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                movingLeft = True
            if event.key == pg.K_RIGHT:
                movingRight = True
            # if event.key == pg.K_SPACE:
            #     shoot = True

            if event.key == pg.K_UP:
                    player_group.sprite.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    movingLeft = False
                if event.key == pg.K_RIGHT:
                    movingRight = False
                # if event.key == pg.K_SPACE:
                #     shoot = False



    if player_group.sprite.hp > 0:
        main_game()
    

    pg.display.update()
    platform_group.draw(screen)
    screen.blit(mainScreen,(0,0))
    clock.tick(60)