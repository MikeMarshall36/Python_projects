import pygame
import math
import random

class Asteroid(object):
    def __init__(self, rank, sw, sh  ):
        self.rank = rank
        if self.rank == 1:
            self.image = pygame.image.load('graphics/asteroid50.png')
        elif self.rank == 2:
            self.image = pygame.image.load('graphics/asteroid100.png')
        else:
            self.image = pygame.image.load('graphics/asteroid150.png')
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))