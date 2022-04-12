import pygame, sys
from Player import Player
import obstacle
from alien import Alien
from random import *
from Laser import Laser

class Game:
    def __init__(self):
        player_sprite = Player((screen_width/2, screen_height), screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.difficulty = 'peace'
        self.lives = 3
        self.default_lives = 3
        self.live_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.live_x_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('graphics/Pixeled.ttf', 20)
        self.heal = True

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_pos = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_pos, x_start=screen_width/15, y_start=610)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=8, cols=12)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        self.screen_shown = False

    def create_obstacle(self, x_start, y_start, x_offset):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + x_offset
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for x_offset in offset:
            self.create_obstacle(x_start, y_start, x_offset)

    def alien_setup(self, rows, cols, x_dist = 65, y_dist = 48, x_offset = 225, y_offset = 49):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_offset
                y = row_index * y_dist + y_offset
                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 3:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)

                self.aliens.add(alien_sprite)

    def alien_position_check(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))


    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()


                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()

        if self.alien_lasers:
            for alien_laser in self.alien_lasers:
                if pygame.sprite.spritecollide(alien_laser, self.blocks, True):
                    alien_laser.kill()

                if pygame.sprite.spritecollide(alien_laser, self.player, False):
                    alien_laser.kill()
                    self.lives -= 1
                    if self.lives <= 0 and self.screen_shown == True:
                        print(f'Game over\nYour score: {self.score}')
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                        pygame.quit()
                        sys.exit()

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10, -10))
        screen.blit(score_surf, score_rect)
        if self.score >= 5400 and self.heal == True and self.lives < self.default_lives:
            self.lives += 1
            self.heal = False
            print('Heath recovered')

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render(f'Victory! Your score is: {self.score} !', False, 'yellow')
            victory_rect = victory_surf.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(victory_surf, victory_rect)
            self.screen_shown = True

    def lose_message(self):
        if self.lives <= 0:
            lose_surf = self.font.render(f'Game over', False, 'red')
            lose_rect = lose_surf.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(lose_surf, lose_rect)
            self.screen_shown = True

    def get_input_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F12]:
            self.player.sprite.laser_cooldown = 6
            self.lives = 666
            self.score += 5008
            print('cheat activated')

    def run(self):
        #updates
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        self.collision_checks()

        #screens
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)

        #others
        self.alien_position_check()
        self.display_lives()
        self.display_score()
        self.victory_message()
        self.lose_message()
        self.get_input_keys()

if __name__ == '__main__':
    pygame.init()
    screen_width = 1200
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    if game.difficulty == 'hell':
        print('hell')
        ALIEN_LASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIEN_LASER, 20)


    if game.difficulty == 'vietnam':
        ALIEN_LASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIEN_LASER, 400)

    if game.difficulty == 'peace':
        ALIEN_LASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIEN_LASER, 800)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIEN_LASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
