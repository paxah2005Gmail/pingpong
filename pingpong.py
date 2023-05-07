#Создай собственный Пинг-Понг!
from random import randint
from pygame import *
from time import time as tm
w_width = 1280
w_height = 960
window = display.set_mode((w_width, w_height))
display.set_caption('Пинг-Понг')
bgColor = (247,242,26)
clock = time.Clock()
font.init()

font2 = font.SysFont('Arial', 100)
rightLabel = font2.render('RIGHT WON!', True, (0, 0, 0))
leftLabel = font2.render('LEFT WON!', True, (0, 0, 0))

mixer.init()
mixer.music.load('fon.ogg')
mixer.music.play()
pingSound = mixer.Sound('pingSound.ogg')
#класс Спрайт
class GameSprite(sprite.Sprite):
    def __init__(self, imageName, x, y, speed, sizeX=75, sizeY=75):
        self.image = transform.scale(image.load(imageName), (sizeX, sizeY))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.bSpeed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def moveLP(self):
        keys = key.get_pressed()
        if keys[K_W] and (self.rect.y <= (0 + self.speed)):
            self.rect.y -= self.speed
        if keys[K_S] and (self.rect.y <= (w_height - self.speed - self.rect.height)):
            self.rect.y += self.speed
    def moveRP(self):
        keys = key.get_pressed()
        if keys[K_UP] and (self.rect.y <= (0 + self.speed)):
            self.rect.y -= self.speed
        if keys[K_DOWN] and (self.rect.y <= (w_height - self.speed - self.rect.height)):
            self.rect.y += self.speed
plH = 100
plW = 25
plL = Player('RedPlayer.png', 0, (w_height - plH)//2, 10, plW, plH)
plR = Player('BluPlayer.png', (w_width - plW), (w_height - plH)//2, 10, plW, plH)
#enemies = sprite.Group()
enemies = list()
for i in range(1):
    enemy = Enemy('ufo.png', randint(0, 625), 0, randint(1, 4))
    #enemies.add(enemy)
    enemies.append(enemy)

run = True
finish = False
bullets = list()
shotTime = 0
btwnShtTm = 0.15
score = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
    window.blit(background, (0, 0))
    if not finish:
        pl.move()
        if tm()-shotTime >= btwnShtTm:
            keys = key.get_pressed()
            if keys[K_UP]:
                fireSound.play()
                bullets.append(Bullet('bullet.png',
                        pl.rect.centerx-10, pl.rect.top, 5, 20, 40))        
                shotTime = tm()
        for bullet in bullets:
            bullet.update()
            bullet.reset()
            for enemy in enemies:
                if sprite.collide_rect(bullet, enemy):
                    enemy.respawn()
                    if (score % 10) == 0:
                        enemies.append(Enemy('ufo.png', randint(0, 625), 0, randint(1, 4 + (score // 50))))                    
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 1
                    if score >= 20:
                        #finish = True
                        finish = False
                    break
        pl.reset()
        #enemies.update()
        #enemies.draw()
        for enemy in enemies:
            enemy.update()
            if sprite.collide_rect(pl, enemy):
                #finish = True
                finish = False
            enemy.reset()
    else:
        if score >= 20:
            window.blit(winLabel, (200, 200))
        else:
            window.blit(loseLabel, (180, 200))
    window.blit(font1.render('Щот: ' + str(score), True, (255,255,255)), (0, 0))
    window.blit(font1.render('Прапусчина: ' + str(score_lose), True, (255,255,255)), (0, 30))    
    display.update()
    clock.tick(60)