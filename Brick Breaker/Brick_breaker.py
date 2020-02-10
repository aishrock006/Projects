import pygame
import random
import math
from threading import Thread
import time
import sys
from os import path
vec = pygame.math.Vector2

# define constants
WIDTH = 400
HEIGHT = 500
FPS = 30 # changed to 60 automatically
SLIDER_ACC = 1
SLIDER_FRICTION = -0.12
SLIDER_GRAV = 0

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BRICK_COLOR = (132, 164, 216)
ball_colors =[ (249, 4, 4) , (252, 95, 5) , (243, 252, 5) ,(99, 252, 5) ,
               (5, 252, 235) ,(5, 66, 252) , (144, 5, 252) ,(252, 5, 223),
               (177, 237, 215) , (155, 209, 18) ,(119, 57, 113) ,(96, 44, 30),
               (255, 255, 255) , (170, 175, 167) , (208, 232, 194) ,(194, 203, 232)



              ]

# define no of bricks
BRICKS_X = 6
BRICKS_Y = 7
TOTAL_BRICKS = BRICKS_X * BRICKS_Y

# define no of balls
BALLS = 5

def slow_mo():
    global FPS
    while FPS < 60:
        FPS += 1
        time.sleep(0.02)

def move_slider(self):
    time.sleep(0.5)
    while True:
        clock.tick(90)

        self.acc = vec(0, SLIDER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.QUIT]:
            break
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.acc.x = -SLIDER_ACC
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.acc.x = SLIDER_ACC

        # apply friction
        self.acc.x += self.vel.x * SLIDER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos.x
        # prevent going outside the wall
        if self.rect.right > WIDTH :
            self.rect.right = WIDTH
            self.acc.x = 0
            self.vel.x = 0
        if self.rect.left < 0 :
            self.rect.left = 0
            self.acc.x = 0
            self.vel.x = 0

        pygame.display.update()

# check ball collide with another balls
def check_ball_to_ball_collision():
    for ball1 in balls:
        for ball2 in balls:
            if id(ball1) != id(ball2) and ball1.rect.top < ball2.rect.bottom and ball1.rect.right > ball2.rect.left and ball1.rect.left < ball2.rect.right and ball1.rect.bottom > ball2.rect.top:
                ball1.speedX *= -1.07
                ball1.speedY *= -1.04
                ball2.speedX *= -1.05
                ball2.speedY *= -1.06

# check Ball collide Slider
def check_Ball_Slider_Collision():
    for ball in balls:
        if ball.rect.bottom > slider.rect.top and ball.rect.right > slider.rect.left and ball.rect.left < slider.rect.right and ball.rect.top < slider.rect.bottom:
            if ball.rect.centerx > slider.rect.left and ball.rect.centerx < slider.rect.right :
                ball.speedY = ball.speedY * -1
                ball.speedX += slider.vel.x // 2
            else:
                ball.speedX *= -1
            if ball.rect.centery > slider.rect.bottom:
                ball.speedY = 10
            elif ball.speedY in [-2 , 2]:
                ball.speedY = -4



# check ball collide with Bricks
def check_Brick_Ball_Collision():
    for ball in balls:
        for brick in bricks:
            if ball.rect.top < brick.rect.bottom and ball.rect.right > brick.rect.left and ball.rect.left < brick.rect.right and ball.rect.bottom > brick.rect.top:
                if ball.rect.centerx > brick.rect.left and ball.rect.centerx < brick.rect.right:
                    ball.speedY *= -1
                elif ball.rect.centery > brick.rect.top or ball.rect.centery < brick.rect.bottom:
                    ball.speedX *= -1
                ball.speedX = random.randrange ( -6 if ball.speedX < 0 else 1 , 6 if ball.speedX >= 0 else -1)
                ball.speedY = random.randrange (  -6 if ball.speedY < 0 else 1 , 6 if ball.speedY >= 0 else -1)
                if ball.speedX == 0:
                    ball.speedX = 3
                if ball.speedY == 0:
                    ball.speedY = 3

                random.choice(tile_break_sound).play()

                for i in range(30):
                    mini_brick = Mini_Bricks(brick.rect.left , brick.rect.top ,brick.rect.right , brick.rect.bottom)
                    all_sprites.add(mini_brick)

                brick.kill()



class Ball ( pygame.sprite.Sprite):
    def __init__(self , r =10 , color = GREEN ):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randrange ( 1 , WIDTH - 2 * r)
        self.y = random.randrange ( HEIGHT // 2 + 2 * r  , HEIGHT - 2 * r -30)
        self.image = pygame.Surface(( 2 * r , 2 * r))
        self.image.set_colorkey(BLACK)
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.ball = pygame.draw.circle(self.image , random.choice(ball_colors) , self.rect.center , r)
        self.rect.center = (self.x , self.y)
        #self.rect = self.image.get_rect()
        self.speedX = random.randrange ( -6 , 6)
        self.speedY = random.randrange ( -6 , 6)
        if self.speedX == 0:
            self.speedX = 3
        if self.speedY == 0:
            self.speedY = 3
        #self.image.fill( RED )

        #self.rect.center = ( WIDTH // 2 , HEIGHT - h // 2 - 3 )

    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speedX = - self.speedX
        if self.rect.top <= 0:
            self.speedY = - self.speedY
        if self.speedX == 0:
            self.speedX = 3

        if self.rect.top > HEIGHT:
            self.kill()
            global BALLS
            BALLS -= 1
            if BALLS == 0:
                global running
                running = False


class Slider ( pygame.sprite.Sprite):
    def __init__(self , h = 10 , color = GREEN ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(( WIDTH // 3 , h ))
        self.image.fill( RED )
        self.rect = self.image.get_rect()
        self.rect.center = ( WIDTH // 2 , HEIGHT - h // 2 - 3 )
        self.pos = vec(WIDTH // 2 , HEIGHT - h // 2 - 3)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        #self.speedX = 0
        Thread(target = move_slider , args = (self,)).start()



class Brick(pygame.sprite.Sprite):
    def __init__(self , x , y ,width = WIDTH // (BRICKS_X ) , height = HEIGHT // (2 * BRICKS_Y )):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width , height))
        self.image.fill(BRICK_COLOR)
        #self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mini_Bricks(pygame.sprite.Sprite):
    def __init__(self , x1  , y1  , x2  , y2  ,width = 15 , height = 15):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((random.randrange(1 ,width) , random.randrange(1 ,height)))
        self.image.fill(BRICK_COLOR)
        #self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(x1 , x2)
        self.rect.centery = random.randrange(y1 , y2)
        self.speedX = 0
        #self.speedY = random.randrange(2 , 8)

        self.speedY =  self.rect.width * self.rect.height * 0.3
        if self.speedY <= 2:
            self.speedY = random.randrange(2 , 5)
        '''
        if self.speedY < 2:
            #self.speedY = random.randrange(2 , 6)
            self.speedY =  self.rect.width * self.rect.height * 0.3
        if self.speedY < 1:
            #self.speedY = random.randrange(2 , 6)
            self.speedY =  self.rect.width * self.rect.height * 0.6
        if self.speedY < 0.5:
            #self.speedY = random.randrange(2 , 6)
            self.speedY =  self.rect.width * self.rect.height * 0.9
        '''


    def update(self):
        self.rect.y += self.speedY
        if self.rect.top > HEIGHT:
            self.kill()



# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(( WIDTH , HEIGHT))
screen.set_colorkey(BLACK)
pygame.display.set_caption(" Break breaker ")
clock = pygame.time.Clock()



# adding sprites to Group
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
bricks = pygame.sprite.Group()

# create bricks
x = 1
y = 1
width = WIDTH // BRICKS_X
height = HEIGHT // (2 * BRICKS_Y)
for i in range(0 ,TOTAL_BRICKS):
    brick = Brick(x + width * (i % BRICKS_X) + i % BRICKS_X , y + height * (i // BRICKS_X) + i // BRICKS_X)
    all_sprites.add(brick)
    bricks.add(brick)

slider = Slider()
all_sprites.add(slider)


# create balls
for i in range(BALLS):
    ball = Ball()
    all_sprites.add(ball)
    balls.add(ball)
waiting = True
while waiting:
    clock.tick(FPS)
    screen.fill((0,0,0,0))
    screen.set_alpha(0)
    all_sprites.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYUP:
            waiting = False


# load game sounds
tile_break_sound =[]
for snd in ['tile_break1.wav' , 'tile_break2.wav' , 'tile_break3.wav']:
    tile_break_sound.append(pygame.mixer.Sound(path.join(snd)))

t1 = Thread(target = slow_mo)
t1.start()




# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # check ball collision with Slider
    check_Ball_Slider_Collision()
    check_ball_to_ball_collision()


    # check ball collision with Bricks
    #hits = pygame.sprite.groupcollide(balls , bricks , False , True)
    if len(bricks)== 0:
        running = False
    check_Brick_Ball_Collision()



    # render / draw
    screen.fill((0,0,0))
    all_sprites.draw(screen)


    # after drawing everything flip the display
    pygame.display.flip()


pygame.quit()
