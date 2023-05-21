#Создай собственный Пинг-Понг!
from random import randint
from pygame import *
from time import time as tm
w_width = 1280
w_height = 800
window = display.set_mode((w_width, w_height))
display.set_caption('Пинг-Понг')
bgColor = (255,255,255)
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
        if keys[K_w] and (self.rect.y >= (0 + self.speed)):
            self.rect.y -= self.speed
        if keys[K_s] and (self.rect.y <= (w_height - self.speed - self.rect.height)):
            self.rect.y += self.speed
    def moveRP(self):
        keys = key.get_pressed()
        if keys[K_UP] and (self.rect.y >= (0 + self.speed)):
            self.rect.y -= self.speed
        if keys[K_DOWN] and (self.rect.y <= (w_height - self.speed - self.rect.height)):
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, imageName, x, y, speed, sizeX=75, sizeY=75):
        super().__init__(imageName, x, y, speed, sizeX, sizeY)
        self.speedX = speed
        self.speedY = speed
    def move(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if (self.rect.y <= 0) or ((self.rect.y >= (w_height - self.rect.height))):
            self.speedY *= -1
        #    print(0)
        #    return 0
        if (self.rect.x <= 0):
            print(1)
            return 1
        if ((self.rect.x >= (w_width - self.rect.width))):
            print(2)
            return 2
        return 0
plH = 100
plW = 25
plL = Player('RedPlayer.png', 0, (w_height - plH)//2, 10, plW, plH)
plR = Player('BluePlayer.png', (w_width - plW), (w_height - plH)//2, 10, plW, plH)
ball = Ball('ball.png', plW, (w_height - 35)//2, 7, 35, 35)
run = True
finish = False
res = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False     
    window.fill(bgColor)
    if res == 0:
        if sprite.collide_rect(ball, plL) or sprite.collide_rect(ball, plR):
            ball.speedX *= -1
        res = ball.move()
        plL.moveLP()
        plR.moveRP()   
        ball.reset()    
        plL.reset()
        plR.reset()
    elif res == 1:
        window.blit(rightLabel, ((w_width - 300)//2, (w_height - 100)//2))
    elif res == 2:
        window.blit(leftLabel, ((w_width - 300)//2, (w_height - 100)//2))
    display.update()
    clock.tick(60)