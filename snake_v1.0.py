"""
    作者：陈志豪
    日期：2019/08/11
    版本：v1.0
    实现功能：（1）贪食蛇的基本游戏规则（2）按‘v’变成无敌版
"""


import pygame
from pygame.locals import *
from random import *


class Square(object):
    def __init__(self, a, b):
        self.x = a
        self.y = b
        self.color = (0, 0, 0)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (20*(self.x-1)+1, 20*(self.y-1)+1, 18, 18))


class Body(Square):
    def __init__(self, a, b):
        Square.__init__(self, a, b)
        self.color = (100, 200, 100)


class GoldenBody(Body):
    def __init__(self, a, b):
        Body.__init__(self, a, b)
        self.color = (255, 215, 0)


class Food(Square):
    def __init__(self):
        self.x = randint(1, 32)
        self.y = randint(1, 24)
        self.color = (255, 62, 150)


class Snake(object):
    def __init__(self):
        self.bodies = [Body(16, 10), Body(16, 11)]
        self.body_len = 2
        self.head = self.bodies[0]
        self.tail = self.bodies[-1]
        self.direction = 'up'

    def render(self, surface):
        for body in self.bodies:
            body.render(surface)


def normal(screen, snake, apple):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            return
        screen.fill((255, 255, 255))
        if snake.direction == 'up' or snake.direction == 'down' :
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                snake.direction = 'left'
            elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                snake.direction = 'right'
        elif snake.direction == 'left' or snake.direction == 'right' :
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                snake.direction = 'up'
            elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
                snake.direction = 'down'
        if snake.direction == 'up':
            new_body = Body(snake.head.x, snake.head.y - 1)
            snake.bodies.insert(0, new_body)
        elif snake.direction == 'down':
            new_body = Body(snake.head.x, snake.head.y + 1)
            snake.bodies.insert(0, new_body)
        elif snake.direction == 'left':
            new_body = Body(snake.head.x - 1, snake.head.y)
            snake.bodies.insert(0, new_body)
        elif snake.direction == 'right':
            new_body = Body(snake.head.x + 1, snake.head.y)
            snake.bodies.insert(0, new_body)
        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body_len += 1
            apple = Food()
        snake.bodies = snake.bodies[:snake.body_len]
        snake.head = snake.bodies[0]
        snake.tail = snake.bodies[-1]
        apple.render(screen)
        snake.render(screen)
        pygame.display.update()
        pygame.time.delay(100)
        """"""
        if pressed_keys[K_v]:
            invincible(screen, snake, apple)
        if snake.head.x < 1 or snake.head.x > 32\
             or snake.head.y < 1 or snake.head.y > 24:
             exit()
        for body in snake.bodies[1:]:
            if body.x == snake.head.x and body.y == snake.head.y:
                exit()
        """"""


def invincible(screen, snake, apple):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_h:
                    y = randint(1, 4)
                    if y == 1:
                        snake.head = Square(0, 1)
                        snake.direction = 'right'
                    elif y == 2:
                        snake.head = Square(33, 1)
                        snake.direction = 'left'
                    elif y == 3:
                        snake.head = Square(0, 24)
                        snake.direction = 'right'
                    elif y == 4:
                        snake.head = Square(33, 24)
                        snake.direction = 'left'
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            return
        screen.fill((255, 255, 255))
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            snake.direction = 'up'
        elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
            snake.direction = 'down'
        elif pressed_keys[K_LEFT] or pressed_keys[K_a]:
            snake.direction = 'left'
        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            snake.direction = 'right'
        if snake.direction == 'up':
            new_body = GoldenBody(snake.head.x, snake.head.y - 1)
            snake.bodies.insert(0, new_body)
        elif snake.direction == 'down':
            new_body = GoldenBody(snake.head.x, snake.head.y + 1)
            snake.bodies.insert(0, new_body)
        elif snake.direction == 'left':
            new_body = GoldenBody(snake.head.x - 1, snake.head.y)
            snake.bodies.insert(0, new_body)
        elif snake.direction == 'right':
            new_body = GoldenBody(snake.head.x + 1, snake.head.y)
            snake.bodies.insert(0, new_body)
        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body_len += 1
            apple = Food()
        snake.bodies = snake.bodies[:snake.body_len]
        snake.head = snake.bodies[0]
        snake.tail = snake.bodies[-1]
        apple.render(screen)
        snake.render(screen)
        pygame.display.update()
        pygame.time.delay(60)
        """"""
        if pressed_keys[K_n]:
            normal(screen, snake, apple)
        if pressed_keys[K_u]:
            snake.body_len += 2

        """"""


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('贪食蛇')
    snake = Snake()
    apple = Food()
    normal(screen, snake, apple)


if __name__ == '__main__':
    main()