import math
import datetime
import random
import pygame
from Player import Player
from Bullet import Bullet
from Asteroid import Asteroid
from Star import Star


pygame.init()

sw = 1200
sh = 700

bg = pygame.image.load('graphics/bg.jpg')

pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 5
score = 0
rapidFire = False
rfStart = -1 
highScore = 0
second_level = False
healed = False

def redrawGameWindow():
    win.blit(bg, (0,0))
    font = pygame.font.Font('graphics/Pixeled.ttf', 15)
    livesText = font.render('Lives: ' + str(lives), 1, (255, 0, 0))
    playAgainText = font.render('Press R to restart', 1, (255,255,255))
    scoreText = font.render('Score: ' + str(score), 1, (255,255,255))
    second_level_warning = font.render('Second level active', 1, (254,242,1))
    highScoreText = font.render('High Score: ' + str(highScore), 1, (218, 165, 0))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for s in stars:
        s.draw(win)

    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [sw//2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [sw//2 - 50, 20, 100 - 100*(count - rfStart)/500, 20])

    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
    win.blit(scoreText, (sw- scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    win.blit(highScoreText, (sw - highScoreText.get_width() -25, 35 + scoreText.get_height()))
    if second_level == True:
        win.blit(second_level_warning, (25, 25 + livesText.get_height()))
    pygame.display.update()

player = Player(sw, sh)
playerBullets = []
asteroids = []
stars = []
count = 0

run = True
while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            if second_level == False:
                ran = random.choice([1, 1, 1, 2, 2, 3])
            else:
                ran = random.choice([1, 2, 2, 3, 3, 3])
            asteroids.append(Asteroid(ran, sw, sh))
        if second_level == False:
            if count % 2000 == 0:
                stars.append(Star(sw, sh))
        else:
            if count % 4000 == 0:
                stars.append(Star(sw, sh))

        player.updateLocation(sw, sh)

        for b in playerBullets:
            b.move()
            if b.checkOffScreen(sw, sh):
                playerBullets.pop(playerBullets.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if ( a.x >= player.x - player.w // 2 and a.x <= player.x + player.w // 2 ) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h // 10 and a.y <= player.y + player.h // 10) or (a.y + a.h >= player.y - player.h//10 and a.y + a.h <= player.y + player.h//10):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))

            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            score += 10
                            na1 = Asteroid(2, sw, sh)
                            na2 = Asteroid(2, sw, sh)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 20
                            na1 = Asteroid(1, sw, sh)
                            na2 = Asteroid(1, sw, sh)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if score >= 8000:
            second_level = True
            if healed == False:
                lives = 2
                healed = True

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in playerBullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True


        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.turnRight()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.moveForward()
        elif not keys[pygame.K_UP] or not keys[pygame.K_w]:
            player.acceleration = 1
            player.img = pygame.image.load(f'graphics/Ship1.png')
        if keys[pygame.K_SPACE]:
            if rapidFire:
                b.color = (254, 242, 1)
                playerBullets.append(Bullet(sw, sh, player.head, player.cosine, player.sine))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        if second_level == False:
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine, player.sine))
                        else:
                            b.color = (133, 255, 1)
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine, player.sine))
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine + (random.uniform(0, 0.9,)), player.sine))
                            b.color = (133, 255, 1)
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine - (random.uniform(0, 0.9)), player.sine))
                            b.color = (133, 255, 1)
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine, player.sine))
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine + (random.uniform(0, 0.9)), player.sine))
                            b.color = (133, 255, 1)
                            playerBullets.append(Bullet(sw, sh, player.head, player.cosine - (random.uniform(0, 0.9)), player.sine))

            if event.key == pygame.K_r:
                if gameover:
                    gameover = False
                    if score >= 5000:
                        lives = 8
                    else:
                        lives = 5
                    player.img = pygame.image.load(f'graphics/Ship1.png')
                    asteroids.clear()
                    stars.clear()
                    second_level = False
                    if score > highScore:
                        highScore = score
                        f = open('High_scores.txt', 'a')
                        f.write(f'{datetime.datetime.now()} Score: {highScore}\n')
                    score = 0

    redrawGameWindow()
pygame.quit()