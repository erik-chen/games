"""
    作者：陈志豪
    日期：2019/08/11
    版本：v1.0
    实现功能：俄罗斯方块的基本游戏规则
"""


import pygame
from pygame.locals import *
from random import *


class Square(object):
    def __init__(self, a, b):
        self.x = a
        self.y = b
        self.color = (0, 0, 0)

    def fall(self):
        self.y += 1

    def de_fall(self):
        self.y -= 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (42*(self.x-1)+101, 42*(self.y-1)+4, 40, 40))

    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)


colors = [(64, 224, 208),
         (0, 0, 205),
         (238, 180, 34),
         (238, 238, 0),
         (50, 205, 50),
         (138, 43, 226),
         (238, 44, 44)]


def check_disappear(earth, dictionary, score):
    rest = 0
    for i in range(1, 20):
        l = []
        for k in dictionary.keys():
            if k[1] == i and dictionary[k[0], i] == 1:
                l.append(k[0])
        if l == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            rest += 1
            print('发现新大陆！')
            for m in l:
                dictionary[m, i] = 0
                for n in earth.squares:
                    if n.x == m and n.y == i:
                        earth.squares.remove(n)
            for p in range(i, 1, -1):
                for k in dictionary.keys():
                    if k[1] == p:
                        dictionary[k[0], p] = dictionary[k[0], p-1]
            for q in l:
                dictionary[q, 1] = 0
            for r in range(i, 1, -1):
                for s in earth.squares:
                    if s.y == r:
                        s.fall()
    if rest == 1:
        score += 100
    elif rest == 2:
        score += 300
    elif rest == 3:
        score += 600
    elif rest == 4:
        score += 1000
    return score


class Tetris(object):
    def __init__(self, a, b, c, d):
        self.squares = [a, b, c, d]
        self.square1 = a
        self.square2 = b
        self.square3 = c
        self.square4 = d
        self.color = choice(colors)
        self.square1.color = self.color
        self.square2.color = self.color
        self.square3.color = self.color
        self.square4.color = self.color

    def fall(self, earth, dictionary, next_tetris, score):
        for square in self.squares:
            square.fall()
        for square in self.squares:
            if dictionary[(square.x, square.y)] == 1:
                for square in self.squares:
                    square.de_fall()
                    dictionary[(square.x, square.y)] = 1
                earth.add(self)
                score = check_disappear(earth, dictionary, score)
                self = next_tetris
                next_tetris = choice([IShape(), LeftLShape(), LShape(), OShape(), LeftZShape(), ZShape(), TShape()])
                break
        return self, next_tetris, score

    def left(self, dictionary):
        for square in self.squares:
            square.left()
        for square in self.squares:
            if (square.x, square.y) not in dictionary or dictionary[(square.x, square.y)] == 1:
                for square in self.squares:
                    square.right()
                break

    def right(self, dictionary):
        for square in self.squares:
            square.right()
        for square in self.squares:
            if (square.x, square.y) not in dictionary or dictionary[(square.x, square.y)] == 1:
                for square in self.squares:
                    square.left()
                break

    def rotate(self, dictionary):
        a = max(self.square1.x, self.square2.x, self.square3.x, self.square4.x)
        b = min(self.square1.y, self.square2.y, self.square3.y, self.square4.y)
        c = min(self.square1.x, self.square2.x, self.square3.x, self.square4.x)
        kk = []
        color = self.color
        for square in self.squares:
            new_x = square.y-b+1-(a-c+1)+a
            new_y = -(square.x-a-1)+b-1
            kk.append([new_x, new_y])
        for i in kk:
            if (i[0], i[1]) not in dictionary or dictionary[(i[0], i[1])] == 1:
                return self
        self = Tetris(Square(kk[0][0], kk[0][1]), Square(kk[1][0], kk[1][1]),
                          Square(kk[2][0], kk[2][1]), Square(kk[3][0], kk[3][1]))
        self.color = color
        self.square1.color = self.color
        self.square2.color = self.color
        self.square3.color = self.color
        self.square4.color = self.color
        return self


    def render(self, surface):
        for square in self.squares:
            square.render(surface)
            

class IShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(3, 1), Square(4, 1), Square(5, 1), Square(6, 1))


class LeftLShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(4, 1), Square(5, 1), Square(6, 1), Square(4, 0))


class LShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(4, 1), Square(5, 1), Square(6, 1), Square(6, 0))


class OShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(4, 1), Square(5, 1), Square(5, 0), Square(4, 0))


class LeftZShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(5, 1), Square(6, 1), Square(4, 0), Square(5, 0))


class ZShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(4, 1), Square(5, 1), Square(5, 0), Square(6, 0))


class TShape(Tetris):
    def __init__(self):
        Tetris.__init__(self, Square(4, 1), Square(5, 1), Square(6, 1), Square(5, 0))


class Earth(object):
    def __init__(self):
        self.squares = []

    def add(self, tetris):
        for square in tetris.squares:
            self.squares.append(square)

    def render(self, surface):
        for square in self.squares:
            square.render(surface)


def main():
    # 设置初始GUI
    pygame.init()
    screen = pygame.display.set_mode((1080, 810), 0, 32)
    pygame.display.set_caption('俄罗斯方块')
    # 设置初始变量
    moving_tetris = choice([IShape(), LeftLShape(), LShape(), OShape(), LeftZShape(), ZShape(), TShape()])
    next_tetris = choice([IShape(), LeftLShape(), LShape(), OShape(), LeftZShape(), ZShape(), TShape()])
    score = 0
    dexterity = 1
    dexterity_times = 5
    earth = Earth()
    # Nettizen_TRIAL_font_100 = pygame.font.Font('Nettizen_TRIAL.ttf', 100)
    # Nettizen_TRIAL_font_120 = pygame.font.SysFont('arial', 100)
    dictionary_key = [(x, y) for y in range(1, 21) for x in range(1, 11)]
    dictionary = {}
    for k in dictionary_key[:190]:
        dictionary[k] = 0
    for k in dictionary_key[-10:]:
        dictionary[k] = 1

    # 进入动画循环
    background = []
    for x in range(1, 11):
        for y in range(1, 20):
            background_square = Square(x, y)
            background_square.color = (180, 180, 180)
            background.append(background_square)

    while True:
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                moving_tetris = moving_tetris.rotate(dictionary)
        dexterity += 1
        if dexterity % dexterity_times == 0:
            moving_tetris, next_tetris, score = moving_tetris.fall(earth, dictionary, next_tetris, score)
            if 1000 <= score < 3000:
                dexterity_times = 4
            elif 3000 <= score < 5000:
                dexterity_times = 3
            elif 5000 <= score < 10000:
                dexterity_times = 2
            elif 10000 <= score:
                dexterity_times = 1

        for test_no in range(1, 21):
            test_set = set(range(1, 11))
            for square_in_earth in earth.squares:
                if square_in_earth.y == test_no:
                    test_set -= {square_in_earth.x}
            if test_set == set():
                Square(1, 1).render(screen)

        if pressed_keys[K_ESCAPE]:
            exit()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            moving_tetris.left(dictionary)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            moving_tetris.right(dictionary)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            moving_tetris, next_tetris, score = moving_tetris.fall(earth, dictionary, next_tetris, score)
            if 1000 <= score < 3000:
                dexterity_times = 4
            elif 3000 <= score < 5000:
                dexterity_times = 3
            elif 5000 <= score < 7000:
                dexterity_times = 2
            elif 7000 <= score:
                dexterity_times = 1
        if pressed_keys[K_SPACE]:
            while True:
                screen.fill((255, 255, 255))
                for background_square in background:
                    background_square.render(screen)

                earth.render(screen)
                moving_tetris.render(screen)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    elif event.key == K_b:
                        break


                pygame.time.delay(80)




        # 设置动画和帧数
        # score_surface = Nettizen_TRIAL_font_100.render('SCORE:', True, (0, 0, 0), (255, 255, 255))
        # score_number_surface = Nettizen_TRIAL_font_120.render('%d' % score, True, (0, 0, 0), (255, 255, 255))
        screen.fill((255, 255, 255))
        # screen.blit(score_surface, (600, 300))
        # screen.blit(score_number_surface, (620, 400))
        for background_square in background:
            background_square.render(screen)
        for square in next_tetris.squares:
            k = Square(square.x+10, square.y+5)
            k.color = next_tetris.color
            k.render(screen)

        earth.render(screen)
        moving_tetris.render(screen)
        pygame.display.update()
        pygame.time.delay(80)


if __name__ == '__main__':
    main()
