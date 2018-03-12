# -*- coding: utf-8 -*-
'''
@time： 2018/3/11
@author: RuiQing Chen
@definition:
'''


class move():
    def __init__(self, last_x, last_y, x, y, arr_x, arr_y, value):
        self.last_x = last_x
        self.last_y = last_y
        self.x = x
        self.y = y
        self.arr_x = arr_x
        self.arr_y = arr_y
        self.value = value


class moveGenerator():
    def __init__(self, chessbroad, status, valuecoord):
        self.chessbroad = chessbroad
        self.status = status
        self.valuecoord = valuecoord

    def collectAllMove(self):
        self.moveCount = 0
        self.allMove = []
        flag = 0 if self.status == 3 else 1
        for coord in self.valuecoord[flag]:
            x = coord[0]
            y = coord[1]
            step = 1
            while self.chessbroad[(x - step, y - step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x - step, y - step)
                step += 1
            step = 1
            while self.chessbroad[(x - step, y)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x - step, y)
                step += 1
            step = 1
            while self.chessbroad[(x - step, y + step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x - step, y + step)
                step += 1

            step = 1
            while self.chessbroad[(x, y - step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x, y - step)
                step += 1
            step = 1
            while self.chessbroad[(x, y + step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x, y + step)
                step += 1

            step = 1
            while self.chessbroad[(x + step, y - step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x + step, y - step)
                step += 1
            step = 1
            while self.chessbroad[(x + step, y)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x + step, y)
                step += 1
            step = 1
            while self.chessbroad[(x + step, y + step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x + step, y + step)
                step += 1

    def collectAllArrowLocation(self, lx, ly, x, y):
        self.chessbroad[(x, y)] = self.chessbroad[(lx, ly)]
        self.chessbroad[(lx, ly)] = 0
        count = 0
        step = 1
        while self.chessbroad[(x - step, y - step)] == 0:
            self.allMove.append(move(lx, ly, x, y, x - step, y - step, 0))
            step += 1
            count += 1
        step = 1
        while self.chessbroad[(x - step, y)] == 0:
            self.allMove.append(move(lx, ly, x, y, x - step, y, 0))
            step += 1
            count += 1
        step = 1
        while self.chessbroad[(x - step, y + step)] == 0:
            self.allMove.append(move(lx, ly, x, y, x - step, y + step, 0))
            step += 1
            count += 1

        step = 1
        while self.chessbroad[(x, y - step)] == 0:
            self.allMove.append(move(lx, ly, x, y, x, y - step, 0))
            step += 1
            count += 1
        step = 1
        while self.chessbroad[(x, y + step)] == 0:
            self.allMove.append(move(lx, ly, x, y, x, y + step, 0))
            step += 1
            count += 1

        step = 1
        while self.chessbroad[(x + step, y - step)] == 0:
            self.allMove.append(move(lx, ly, x, y, x + step, y - step, 0))
            step += 1
            count += 1
        step = 1
        while self.chessbroad[(x + step, y)] == 0:
            self.allMove.append(move(lx, ly, x, y, x + step, y, 0))
            step += 1
            count += 1
        step = 1
        while self.chessbroad[(x + step, y + step)] == 0:
            self.allMove.append(move(lx, ly, x, y, x + step, y + step, 0))
            step += 1
            count += 1

        self.chessbroad[(lx, ly)] = self.chessbroad[(x, y)]
        self.chessbroad[(x, y)] = 0
        return count
