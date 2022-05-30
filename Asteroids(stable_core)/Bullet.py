import pygame
import math

class Bullet(object):
    def __init__(self, sw, sh, point, cosine, sine):
        self.point = point
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = cosine
        self.s = sine
        self.xv = self.c * 10
        self.yv = self.s * 10
        self.color = (0, 255, 214)

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

    def checkOffScreen(self, sw, sh):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True