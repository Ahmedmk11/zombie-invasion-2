from random import randrange
import pygame as pg, InGame
pg.init()
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,direction,angle):
        super().__init__()
        self.direction = direction
        self.angle = angle
        self.speed = 20
        self.index = randrange(1,2)
        self.tmp = pg.image.load(f'resources/images/sprites/heroine/{self.index}.png')

        if self.direction == 1:
            self.image = self.tmp
            if InGame.isShootingLeftUp:
                self.image = pg.transform.rotate(self.image, -45)

        if self.direction == -1:
            self.image = pg.transform.flip(self.tmp, True, False)
            if InGame.isShootingRightUp:
                self.image = pg.transform.rotate(self.image,45)


        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.x -= (self.direction * self.speed)
        if self.angle:
            self.rect.y -= self.speed-10
        if self.rect.left >= 1321 or self.rect.right <= -5:  
            self.kill()
        if InGame.bossExists:
            if InGame.level == 6 and InGame.boss.hp > 0 and ((self.direction == 1 and (self.rect.left >= InGame.boss.rect.left) and (self.rect.left - InGame.boss.rect.centerx) < 45) or (self.direction == -1 and (InGame.boss.rect.right >= self.rect.right) and (InGame.boss.rect.centerx - self.rect.right) < 45)):
                if self.rect.centery > 300:
                    InGame.boss.getDamage(10)
                if self.rect.centery > 87 and self.rect.centery <= 300 or InGame.boss.attacking:
                    InGame.boss.getDamage(20)
                self.kill()

            
        InGame.screen.blit(self.image,self.rect)
        