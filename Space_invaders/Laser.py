import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, constraint):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('cyan')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.limit_y = constraint

    # delet laser if it out of screen
    def destroy(self):
        if self.rect.y <= -20 or self.rect.y >= self.limit_y + 20:
            self.kill()


    def update(self):
        self.rect.y += self.speed
        self.destroy()


