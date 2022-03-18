import pygame
import random
pygame.init()

flag = True
acceleration = 0.19
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
FPS = 90
class Ball():
    def __init__(self):
        self.y = 20
        self.velocity = 2
        self.rad = random.randrange(15, 25)

    def draw(self):
        pygame.draw.circle(screen, (20, 20, 20), (750, int(self.y)), self.rad)



    def move(self):
        global acceleration, flag
        self.velocity += acceleration
        self.y += self.velocity
        self.velocity += acceleration
        if self.y >= 301 and flag:
            self.velocity = 1.5
            acceleration = 0
            flag = False
        if self.y >= 598 - self.rad:
            self.velocity = -self.velocity
            acceleration += 0.02
            self.velocity += acceleration
        if self.y >= 599 - self.rad:
            acceleration = 0
            self.velocity = 0


def game():
    ball = Ball()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        ball.move()
        screen.fill((255, 255, 255))
        ball.draw()
        pygame.display.update()
        clock.tick(FPS)
game()
pygame.quit()