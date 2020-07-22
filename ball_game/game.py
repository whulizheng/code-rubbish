import pygame
import random
import time

pygame.init()

RED = 255, 0, 0
ORANGE = 255, 156, 0
YELLOW = 255, 255, 0
GREEN = 0, 255, 0
GREENBLUE = 0, 255, 255
BLUE = 0, 0, 255
PURPLE = 255, 0, 255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
Grey = (37, 37, 37)

myfontLose = pygame.font.Font(None, 70)
myfontRetry = pygame.font.Font(None, 40)
myfontScore = pygame.font.Font(None, 20)

screen_x = 600
screen_y = 800
textImageLose = myfontLose.render("You loser", True, WHITE)
textImageRetry = myfontRetry.render("press space to retry", True, WHITE)
ball1Speed = 8


class ball1:
    def __init__(self):
        self.x = int(screen_x / 2)
        self.y = int(screen_y / 2)
        self.status = 1
        self.timer = 0
        self.antiballs = []
        self.score = 0
        self.anger = 0

    def moveLeft(self):
        self.x -= ball1Speed

    def moveUp(self):
        self.y -= ball1Speed

    def moveDown(self):
        self.y += ball1Speed

    def moveRight(self):
        self.x += ball1Speed

    def display(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 7, 0)
        if self.anger > 12:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), 80, 3)

    def ability(self):
        textImageAbility = myfontRetry.render("press space", True, WHITE)
        screen.blit(textImageAbility, (screen_x / 2, 0))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.anger = 0
            for i in self.antiballs:
                if (i.x - self.x) * (i.x - self.x) + (i.y - self.y) * (
                        i.y - self.y) <= 6400:
                    self.antiballs.remove(i)
                    self.score += 1
            for i in self.antiballs:
                if (i.x - self.x) * (i.x - self.x) + (i.y - self.y) * (
                        i.y - self.y) <= 6400:
                    self.antiballs.remove(i)
                    self.score += 1

    def getStatus(self):
        if self.x > screen_x:
            self.x = screen_x
        if self.x < 0:
            self.x = 0
        if self.y > screen_y:
            self.y = screen_y
        if self.y < 0:
            self.y = 0
        if self.timer == 30:
            self.timer = 0
            newBall = ball2()
            self.antiballs.append(newBall)
            self.score += 1
            self.anger += 1
        for i in self.antiballs:
            i.move()
            i.display()
            if (i.x - self.x) * (i.x - self.x) + (i.y - self.y) * (
                    i.y - self.y) < 100:
                self.status = 0
        self.timer += 1
        if self.anger > 12:
            self.ability()

    def retry(self):
        self.x = int(screen_x / 2)
        self.y = int(screen_y / 2)
        self.status = 1
        self.timer = 0
        self.score = 0
        self.antiballs = []
        self.anger = 0


class ball2:
    def __init__(self):
        self.posNum = random.randint(1, 4)
        if self.posNum == 1:
            self.x = int(screen_x / 4)
            self.y = int(screen_y / 4)
        elif self.posNum == 2:
            self.x = int(screen_x / 4)
            self.y = int(screen_y / 4) * 3
        elif self.posNum == 3:
            self.x = int(screen_x / 4) * 3
            self.y = int(screen_y / 4)
        elif self.posNum == 4:
            self.x = int(screen_x / 4) * 3
            self.y = int(screen_y / 4) * 3
        self.speed = random.randint(1, 4)

    def move(self):
        if self.x < ball1.x:
            self.x += self.speed
        if self.x > ball1.x:
            self.x -= self.speed
        if self.y < ball1.y:
            self.y += self.speed
        if self.y > ball1.y:
            self.y -= self.speed

    def display(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 7, 0)


screen = pygame.display.set_mode((screen_x, screen_y))
pygame.mouse.set_visible(False)
ball1 = ball1()

while True:
    screen.fill(Grey)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    if ball1.status == 0:
        screen.blit(textImageLose, (100, 100))
        screen.blit(textImageRetry, (100, 200))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            ball1.retry()
    elif ball1.status == 1:
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[
                pygame.K_LEFT]:
            ball1.moveLeft()
        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[
                pygame.K_UP]:
            ball1.moveUp()
        if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[
                pygame.K_DOWN]:
            ball1.moveDown()
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[
                pygame.K_RIGHT]:
            ball1.moveRight()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            ball1.status = 2
        ball1.getStatus()
        ball1.display()
        textImageScore = myfontScore.render("score: %d" % ball1.score, True,
                                            WHITE)
        screen.blit(textImageScore, (10, 10))
    elif ball1.status == 2:
        textImageSuspend = myfontRetry.render("press space to continue", True,
                                              WHITE)
        screen.blit(textImageSuspend, (100, 300))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            ball1.status = 1

    pygame.display.update()
    # 刷新画面
    time.sleep(0.03)
