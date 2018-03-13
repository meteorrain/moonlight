# -*- coding: utf-8 -*-
# @time： 2018/3/11
# @author: RuiQing Chen
# @definition:


class Move:
    def __init__(self, last_x, last_y, x, y, arr_x, arr_y, value):
        self.last_x = last_x
        self.last_y = last_y
        self.x = x
        self.y = y
        self.arr_x = arr_x
        self.arr_y = arr_y
        self.value = value


class MoveGenerator:
    def __init__(self, chessboard, status, chess_coord):
        self.chessboard = chessboard
        self.status = status
        self.chess_coord = chess_coord

    # 收集所有的走法
    def collectAllMove(self):
        self.moveCount = 0
        self.allMove = []
        flag = self.status
        for coord in self.chess_coord[flag]:
            x = coord[0]
            y = coord[1]
            step = 1
            while self.chessboard[(x - step, y - step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x - step, y - step)
                step += 1
            step = 1
            while self.chessboard[(x - step, y)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x - step, y)
                step += 1
            step = 1
            while self.chessboard[(x - step, y + step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x - step, y + step)
                step += 1

            step = 1
            while self.chessboard[(x, y - step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x, y - step)
                step += 1
            step = 1
            while self.chessboard[(x, y + step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x, y + step)
                step += 1

            step = 1
            while self.chessboard[(x + step, y - step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x + step, y - step)
                step += 1
            step = 1
            while self.chessboard[(x + step, y)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x + step, y)
                step += 1
            step = 1
            while self.chessboard[(x + step, y + step)] == 0:
                self.moveCount += self.collectAllArrowLocation(x, y, x + step, y + step)
                step += 1

    # 收集当前棋子移动下所有放置障碍的方法
    def collectAllArrowLocation(self, lx, ly, x, y):
        self.chessboard[(x, y)] = self.chessboard[(lx, ly)]
        self.chessboard[(lx, ly)] = 0
        count = 0
        step = 1
        while self.chessboard[(x - step, y - step)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x - step, y - step, 0))
            step += 1
            count += 1
        step = 1
        while self.chessboard[(x - step, y)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x - step, y, 0))
            step += 1
            count += 1
        step = 1
        while self.chessboard[(x - step, y + step)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x - step, y + step, 0))
            step += 1
            count += 1

        step = 1
        while self.chessboard[(x, y - step)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x, y - step, 0))
            step += 1
            count += 1
        step = 1
        while self.chessboard[(x, y + step)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x, y + step, 0))
            step += 1
            count += 1

        step = 1
        while self.chessboard[(x + step, y - step)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x + step, y - step, 0))
            step += 1
            count += 1
        step = 1
        while self.chessboard[(x + step, y)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x + step, y, 0))
            step += 1
            count += 1
        step = 1
        while self.chessboard[(x + step, y + step)] == 0:
            self.allMove.append(Move(lx, ly, x, y, x + step, y + step, 0))
            step += 1
            count += 1

        self.chessboard[(lx, ly)] = self.chessboard[(x, y)]
        self.chessboard[(x, y)] = 0
        return count
