# -*- coding: utf-8 -*-
'''
@time： 2018/3/11
@author: RuiQing Chen
@definition:
'''
from random import choice, randrange
from copy import deepcopy


class randomMove():
    def __init__(self, chessbroad, status, valuecoord):
        self.chessbroad = deepcopy(chessbroad)
        self.status = status
        self.valuecoord = valuecoord
        self.result = []

    def chessMove(self):
        if self.status == 3:
            coord = self.valuecoord[0][:]
        else:
            coord = self.valuecoord[1][:]
        while len(coord):
            select_coord = choice(coord)
            direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            while len(direction):
                select_direct = choice(direction)
                x = select_coord[0]
                y = select_coord[1]
                if select_direct == (-1, -1):
                    step = 1
                    while self.chessbroad[(x - step, y - step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x - d, y - d)
                        return True
                    else:
                        direction.remove((-1, -1))
                elif select_direct == (-1, 0):
                    step = 1
                    while self.chessbroad[(x - step, y)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x - d, y)
                        return True
                    else:
                        direction.remove((-1, 0))
                elif select_direct == (-1, 1):
                    step = 1
                    while self.chessbroad[(x - step, y + step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x - d, y + d)
                        return True
                    else:
                        direction.remove((-1, 1))

                elif select_direct == (0, -1):
                    step = 1
                    while self.chessbroad[(x, y - step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x, y - d)
                        return True
                    else:
                        direction.remove((0, -1))
                elif select_direct == (0, 1):
                    step = 1
                    while self.chessbroad[(x, y + step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x, y + d)
                        return True
                    else:
                        direction.remove((0, 1))

                elif select_direct == (1, -1):
                    step = 1
                    while self.chessbroad[(x + step, y - step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x + d, y - d)
                        return True
                    else:
                        direction.remove((1, -1))
                elif select_direct == (1, 0):
                    step = 1
                    while self.chessbroad[(x + step, y)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x + d, y)
                        return True
                    else:
                        direction.remove((1, 0))
                else:
                    step = 1
                    while self.chessbroad[(x + step, y + step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x + d, y + d)
                        return True
                    else:
                        direction.remove((1, 1))
            coord.remove(select_coord)
        return False

    def arrowShoot(self, lx, ly, x, y):
        self.chessbroad[(x, y)] = self.chessbroad[(lx, ly)]
        self.chessbroad[(lx, ly)] = 0
        direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        while len(direction):
            select_direct = choice(direction)
            if select_direct == (-1, -1):
                step = 1
                while self.chessbroad[(x - step, y - step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x - d, y - d])
                    break
                else:
                    direction.remove((-1, -1))
            elif select_direct == (-1, 0):
                step = 1
                while self.chessbroad[(x - step, y)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x - d, y])
                    break
                else:
                    direction.remove((-1, 0))
            elif select_direct == (-1, 1):
                step = 1
                while self.chessbroad[(x - step, y + step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x - d, y + d])
                    break
                else:
                    direction.remove((-1, 1))

            elif select_direct == (0, -1):
                step = 1
                while self.chessbroad[(x, y - step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x, y - d])
                    break
                else:
                    direction.remove((0, -1))
            elif select_direct == (0, 1):
                step = 1
                while self.chessbroad[(x, y + step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x, y + d])
                    break
                else:
                    direction.remove((0, 1))

            elif select_direct == (1, -1):
                step = 1
                while self.chessbroad[(x + step, y - step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x + d, y - d])
                    break
                else:
                    direction.remove((1, -1))
            elif select_direct == (1, 0):
                step = 1
                while self.chessbroad[(x + step, y)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x + d, y])
                    break
                else:
                    direction.remove((1, 0))
            else:
                step = 1
                while self.chessbroad[(x + step, y + step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result.append([lx, ly, x, y, x + d, y + d])
                    break
                else:
                    direction.remove((1, 1))

        self.chessbroad[(lx, ly)] = self.chessbroad[(x, y)]
        self.chessbroad[(x, y)] = 0
