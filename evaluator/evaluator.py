# -*- coding: utf-8 -*-
# @time： 2018/3/9
# @author: RuiQing Chen
# @definition:

from math import fabs


class Evaluator:
    def __init__(self, chessboard, status, chess_coord):
        self.chessboard = chessboard
        self.status = status
        self.chess_coord = chess_coord
        self.kingMovePositive = {}
        self.kingMoveNegative = {}
        self.queenMovePositive = {}
        self.queenMoveNegative = {}
        self.kingTraverse()
        self.queenTraverse()
        self.computeValue()

    # 国王移动法棋盘估值
    def kingTraverse(self):
        for x in range(1, 11):
            for y in range(1, 11):
                self.kingMovePositive[(x, y)] = 0
                self.kingMoveNegative[(x, y)] = 0
        PositiveCollect = []
        NegativeCollect = []
        for i in range(0, 7, 2):
            x = self.chess_coord[0][i]
            y = self.chess_coord[0][i + 1]
            if self.chessboard[x - 1][y - 1] == 0 and self.kingMovePositive[
                (x - 1, y - 1)] == 0:
                self.kingMovePositive[(x - 1, y - 1)] = 1
                PositiveCollect.append((x - 1, y - 1))
            if self.chessboard[x - 1][y] == 0 and self.kingMovePositive[(x - 1, y)] == 0:
                self.kingMovePositive[(x - 1, y)] = 1
                PositiveCollect.append((x - 1, y))
            if self.chessboard[x - 1][y + 1] == 0 and self.kingMovePositive[
                (x - 1, y + 1)] == 0:
                self.kingMovePositive[(x - 1, y + 1)] = 1
                PositiveCollect.append((x - 1, y + 1))

            if self.chessboard[x][y - 1] == 0 and self.kingMovePositive[(x, y - 1)] == 0:
                self.kingMovePositive[(x, y - 1)] = 1
                PositiveCollect.append((x, y - 1))
            if self.chessboard[x][y + 1] == 0 and self.kingMovePositive[(x, y + 1)] == 0:
                self.kingMovePositive[(x, y + 1)] = 1
                PositiveCollect.append((x, y + 1))

            if self.chessboard[x + 1][y - 1] == 0 and self.kingMovePositive[
                (x + 1, y - 1)] == 0:
                self.kingMovePositive[(x + 1, y - 1)] = 1
                PositiveCollect.append((x + 1, y - 1))
            if self.chessboard[x + 1][y] == 0 and self.kingMovePositive[(x + 1, y)] == 0:
                self.kingMovePositive[(x + 1, y)] = 1
                PositiveCollect.append((x + 1, y))
            if self.chessboard[x + 1][y + 1] == 0 and self.kingMovePositive[
                (x + 1, y + 1)] == 0:
                self.kingMovePositive[(x + 1, y + 1)] = 1
                PositiveCollect.append((x + 1, y + 1))

        for i in range(0, 7, 2):
            x = self.chess_coord[1][i]
            y = self.chess_coord[1][i + 1]
            if self.chessboard[x - 1][y - 1] == 0 and self.kingMoveNegative[
                (x - 1, y - 1)] == 0:
                self.kingMoveNegative[(x - 1, y - 1)] = 1
                NegativeCollect.append((x - 1, y - 1))
            if self.chessboard[x - 1][y] == 0 and self.kingMoveNegative[(x - 1, y)] == 0:
                self.kingMoveNegative[(x - 1, y)] = 1
                NegativeCollect.append((x - 1, y))
            if self.chessboard[x - 1][y + 1] == 0 and self.kingMoveNegative[
                (x - 1, y + 1)] == 0:
                self.kingMoveNegative[(x - 1, y + 1)] = 1
                NegativeCollect.append((x - 1, y + 1))

            if self.chessboard[x][y - 1] == 0 and self.kingMoveNegative[(x, y - 1)] == 0:
                self.kingMoveNegative[(x, y - 1)] = 1
                NegativeCollect.append((x, y - 1))
            if self.chessboard[x][y + 1] == 0 and self.kingMoveNegative[(x, y + 1)] == 0:
                self.kingMoveNegative[(x, y + 1)] = 1
                NegativeCollect.append((x, y + 1))

            if self.chessboard[x + 1][y - 1] == 0 and self.kingMoveNegative[
                (x + 1, y - 1)] == 0:
                self.kingMoveNegative[(x + 1, y - 1)] = 1
                NegativeCollect.append((x + 1, y - 1))
            if self.chessboard[x + 1][y] == 0 and self.kingMoveNegative[(x + 1, y)] == 0:
                self.kingMoveNegative[(x + 1, y)] = 1
                NegativeCollect.append((x + 1, y))
            if self.chessboard[x + 1][y + 1] == 0 and self.kingMoveNegative[
                (x + 1, y + 1)] == 0:
                self.kingMoveNegative[(x + 1, y + 1)] = 1
                NegativeCollect.append((x + 1, y + 1))
        nextCoord = []
        for n in range(2, 9):
            nextCoord.clear()
            for coord in PositiveCollect:
                x = coord[0]
                y = coord[1]
                if self.chessboard[x - 1][y - 1] == 0 and (
                        self.kingMovePositive[(x - 1, y - 1)] > n or
                        self.kingMovePositive[(x - 1, y - 1)] == 0):
                    nextCoord.append((x - 1, y - 1))
                    self.kingMovePositive[(x - 1, y - 1)] = n
                if self.chessboard[x - 1][y] == 0 and (
                        self.kingMovePositive[(x - 1, y)] > n or
                        self.kingMovePositive[(x - 1, y)] == 0):
                    nextCoord.append((x - 1, y))
                    self.kingMovePositive[(x - 1, y)] = n
                if self.chessboard[x - 1][y + 1] == 0 and (
                        self.kingMovePositive[(x - 1, y + 1)] > n or
                        self.kingMovePositive[(x - 1, y + 1)] == 0):
                    nextCoord.append((x - 1, y + 1))
                    self.kingMovePositive[(x - 1, y + 1)] = n

                if self.chessboard[x][y - 1] == 0 and (
                        self.kingMovePositive[(x, y - 1)] > n or
                        self.kingMovePositive[(x, y - 1)] == 0):
                    nextCoord.append((x, y - 1))
                    self.kingMovePositive[(x, y - 1)] = n
                if self.chessboard[x][y + 1] == 0 and (
                        self.kingMovePositive[(x, y + 1)] > n or
                        self.kingMovePositive[(x, y + 1)] == 0):
                    nextCoord.append((x, y + 1))
                    self.kingMovePositive[(x, y + 1)] = n

                if self.chessboard[x + 1][y - 1] == 0 and (
                        self.kingMovePositive[(x + 1, y - 1)] > n or
                        self.kingMovePositive[(x + 1, y - 1)] == 0):
                    nextCoord.append((x + 1, y - 1))
                    self.kingMovePositive[(x + 1, y - 1)] = n
                if self.chessboard[x + 1][y] == 0 and (
                        self.kingMovePositive[(x + 1, y)] > n or
                        self.kingMovePositive[(x + 1, y)] == 0):
                    nextCoord.append((x + 1, y))
                    self.kingMovePositive[(x + 1, y)] = n
                if self.chessboard[x + 1][y + 1] == 0 and (
                        self.kingMovePositive[(x + 1, y + 1)] > n or
                        self.kingMovePositive[(x + 1, y + 1)] == 0):
                    nextCoord.append((x + 1, y + 1))
                    self.kingMovePositive[(x + 1, y + 1)] = n
            PositiveCollect.clear()
            PositiveCollect = nextCoord[:]
            nextCoord.clear()
            for coord in NegativeCollect:
                x = coord[0]
                y = coord[1]
                if self.chessboard[x - 1][y - 1] == 0 and (
                        self.kingMoveNegative[(x - 1, y - 1)] > n or
                        self.kingMoveNegative[(x - 1, y - 1)] == 0):
                    nextCoord.append((x - 1, y - 1))
                    self.kingMoveNegative[(x - 1, y - 1)] = n
                if self.chessboard[x - 1][y] == 0 and (
                        self.kingMoveNegative[(x - 1, y)] > n or
                        self.kingMoveNegative[(x - 1, y)] == 0):
                    nextCoord.append((x - 1, y))
                    self.kingMoveNegative[(x - 1, y)] = n
                if self.chessboard[x - 1][y + 1] == 0 and (
                        self.kingMoveNegative[(x - 1, y + 1)] > n or
                        self.kingMoveNegative[(x - 1, y + 1)] == 0):
                    nextCoord.append((x - 1, y + 1))
                    self.kingMoveNegative[(x - 1, y + 1)] = n

                if self.chessboard[x][y - 1] == 0 and (
                        self.kingMoveNegative[(x, y - 1)] > n or
                        self.kingMoveNegative[(x, y - 1)] == 0):
                    nextCoord.append((x, y - 1))
                    self.kingMoveNegative[(x, y - 1)] = n
                if self.chessboard[x][y + 1] == 0 and (
                        self.kingMoveNegative[(x, y + 1)] > n or
                        self.kingMoveNegative[(x, y + 1)] == 0):
                    nextCoord.append((x, y + 1))
                    self.kingMoveNegative[(x, y + 1)] = n

                if self.chessboard[x + 1][y - 1] == 0 and (
                        self.kingMoveNegative[(x + 1, y - 1)] > n or
                        self.kingMoveNegative[(x + 1, y - 1)] == 0):
                    nextCoord.append((x + 1, y - 1))
                    self.kingMoveNegative[(x + 1, y - 1)] = n
                if self.chessboard[x + 1][y] == 0 and (
                        self.kingMoveNegative[(x + 1, y)] > n or
                        self.kingMoveNegative[(x + 1, y)] == 0):
                    nextCoord.append((x + 1, y))
                    self.kingMoveNegative[(x + 1, y)] = n
                if self.chessboard[x + 1][y + 1] == 0 and (
                        self.kingMoveNegative[(x + 1, y + 1)] > n or
                        self.kingMoveNegative[(x + 1, y + 1)] == 0):
                    nextCoord.append((x + 1, y + 1))
                    self.kingMoveNegative[(x + 1, y + 1)] = n
            NegativeCollect.clear()
            NegativeCollect = nextCoord[:]

    # 皇后移动法棋盘估值
    def queenTraverse(self):
        for x in range(1, 11):
            for y in range(1, 11):
                self.queenMovePositive[(x, y)] = 0
                self.queenMoveNegative[(x, y)] = 0
        PositiveCollect = []
        NegativeCollect = []
        for i in range(0, 7, 2):
            x = self.chess_coord[0][i]
            y = self.chess_coord[0][i + 1]
            step = 1
            while self.chessboard[x - step][y - step] == 0:
                if self.queenMovePositive[(x - step, y - step)] == 0:
                    self.queenMovePositive[(x - step, y - step)] = 1
                    PositiveCollect.append((x - step, y - step))
                step += 1
            step = 1
            while self.chessboard[x - step][y] == 0:
                if self.queenMovePositive[(x - step, y)] == 0:
                    self.queenMovePositive[(x - step, y)] = 1
                    PositiveCollect.append((x - step, y))
                step += 1
            step = 1
            while self.chessboard[x - step][y + step] == 0:
                if self.queenMovePositive[(x - step, y + step)] == 0:
                    self.queenMovePositive[(x - step, y + step)] = 1
                    PositiveCollect.append((x - step, y + step))
                step += 1

            step = 1
            while self.chessboard[x][y - step] == 0:
                if self.queenMovePositive[(x, y - step)] == 0:
                    self.queenMovePositive[(x, y - step)] = 1
                    PositiveCollect.append((x, y - step))
                step += 1
            step = 1
            while self.chessboard[x][y + step] == 0:
                if self.queenMovePositive[(x, y + step)] == 0:
                    self.queenMovePositive[(x, y + step)] = 1
                    PositiveCollect.append((x, y + step))
                step += 1

            step = 1
            while self.chessboard[x + step][y - step] == 0:
                if self.queenMovePositive[(x + step, y - step)] == 0:
                    self.queenMovePositive[(x + step, y - step)] = 1
                    PositiveCollect.append((x + step, y - step))
                step += 1
            step = 1
            while self.chessboard[x + step][y] == 0:
                if self.queenMovePositive[(x + step, y)] == 0:
                    self.queenMovePositive[(x + step, y)] = 1
                    PositiveCollect.append((x + step, y))
                step += 1
            step = 1
            while self.chessboard[x + step][y + step] == 0:
                if self.queenMovePositive[(x + step, y + step)] == 0:
                    self.queenMovePositive[(x + step, y + step)] = 1
                    PositiveCollect.append((x + step, y + step))
                step += 1

        for i in range(0, 7, 2):
            x = self.chess_coord[1][i]
            y = self.chess_coord[1][i + 1]
            step = 1
            while self.chessboard[x - step][y - step] == 0:
                if self.queenMoveNegative[(x - step, y - step)] == 0:
                    self.queenMoveNegative[(x - step, y - step)] = 1
                    NegativeCollect.append((x - step, y - step))
                step += 1
            step = 1
            while self.chessboard[x - step][y] == 0:
                if self.queenMoveNegative[(x - step, y)] == 0:
                    self.queenMoveNegative[(x - step, y)] = 1
                    NegativeCollect.append((x - step, y))
                step += 1
            step = 1
            while self.chessboard[x - step][y + step] == 0:
                if self.queenMoveNegative[(x - step, y + step)] == 0:
                    self.queenMoveNegative[(x - step, y + step)] = 1
                    NegativeCollect.append((x - step, y + step))
                step += 1

            step = 1
            while self.chessboard[x][y - step] == 0:
                if self.queenMoveNegative[(x, y - step)] == 0:
                    self.queenMoveNegative[(x, y - step)] = 1
                    NegativeCollect.append((x, y - step))
                step += 1
            step = 1
            while self.chessboard[x][y + step] == 0:
                if self.queenMoveNegative[(x, y + step)] == 0:
                    self.queenMoveNegative[(x, y + step)] = 1
                    NegativeCollect.append((x, y + step))
                step += 1

            step = 1
            while self.chessboard[x + step][y - step] == 0:
                if self.queenMoveNegative[(x + step, y - step)] == 0:
                    self.queenMoveNegative[(x + step, y - step)] = 1
                    NegativeCollect.append((x + step, y - step))
                step += 1
            step = 1
            while self.chessboard[x + step][y] == 0:
                if self.queenMoveNegative[(x + step, y)] == 0:
                    self.queenMoveNegative[(x + step, y)] = 1
                    NegativeCollect.append((x + step, y))
                step += 1
            step = 1
            while self.chessboard[x + step][y + step] == 0:
                if self.queenMoveNegative[(x + step, y + step)] == 0:
                    self.queenMoveNegative[(x + step, y + step)] = 1
                    NegativeCollect.append((x + step, y + step))
                step += 1

        nextCoord = []
        for n in range(2, 6):
            nextCoord.clear()
            for coord in PositiveCollect:
                x = coord[0]
                y = coord[1]
                step = 1
                while self.chessboard[x - step][y - step] == 0 and (
                        self.queenMovePositive[(x - step, y - step)] == 0 or self.queenMovePositive[
                    (x - step, y - step)] > n):
                    self.queenMovePositive[(x - step, y - step)] = n
                    nextCoord.append((x - step, y - step))
                    step += 1
                step = 1
                while self.chessboard[x - step][y] == 0 and (
                        self.queenMovePositive[(x - step, y)] == 0 or self.queenMovePositive[(x - step, y)] > n):
                    self.queenMovePositive[(x - step, y)] = n
                    nextCoord.append((x - step, y))
                    step += 1
                step = 1
                while self.chessboard[x - step][y + step] == 0 and (
                        self.queenMovePositive[(x - step, y + step)] == 0 or self.queenMovePositive[
                    (x - step, y + step)] > n):
                    self.queenMovePositive[(x - step, y + step)] = n
                    nextCoord.append((x - step, y + step))
                    step += 1

                step = 1
                while self.chessboard[x][y - step] == 0 and (
                        self.queenMovePositive[(x, y - step)] == 0 or self.queenMovePositive[(x, y - step)] > n):
                    self.queenMovePositive[(x, y - step)] = n
                    nextCoord.append((x, y - step))
                    step += 1
                step = 1
                while self.chessboard[x][y + step] == 0 and (
                        self.queenMovePositive[(x, y + step)] == 0 or self.queenMovePositive[(x, y + step)] > n):
                    self.queenMovePositive[(x, y + step)] = n
                    nextCoord.append((x, y + step))
                    step += 1

                step = 1
                while self.chessboard[x + step][y - step] == 0 and (
                        self.queenMovePositive[(x + step, y - step)] == 0 or self.queenMovePositive[
                    (x + step, y - step)] > n):
                    self.queenMovePositive[(x + step, y - step)] = n
                    nextCoord.append((x + step, y - step))
                    step += 1
                step = 1
                while self.chessboard[x + step][y] == 0 and (
                        self.queenMovePositive[(x + step, y)] == 0 or self.queenMovePositive[(x + step, y)] > n):
                    self.queenMovePositive[(x + step, y)] = n
                    nextCoord.append((x + step, y))
                    step += 1
                step = 1
                while self.chessboard[x + step][y + step] == 0 and (
                        self.queenMovePositive[(x + step, y + step)] == 0 or self.queenMovePositive[
                    (x + step, y + step)] > n):
                    self.queenMovePositive[(x + step, y + step)] = n
                    nextCoord.append((x + step, y + step))
                    step += 1

            PositiveCollect.clear()
            PositiveCollect = nextCoord[:]
            nextCoord.clear()

            for coord in NegativeCollect:
                x = coord[0]
                y = coord[1]
                step = 1
                while self.chessboard[x - step][y - step] == 0 and (
                        self.queenMoveNegative[(x - step, y - step)] == 0 or self.queenMoveNegative[
                    (x - step, y - step)] > n):
                    self.queenMoveNegative[(x - step, y - step)] = n
                    nextCoord.append((x - step, y - step))
                    step += 1
                step = 1
                while self.chessboard[x - step][y] == 0 and (
                        self.queenMoveNegative[(x - step, y)] == 0 or self.queenMoveNegative[(x - step, y)] > n):
                    self.queenMoveNegative[(x - step, y)] = n
                    nextCoord.append((x - step, y))
                    step += 1
                step = 1
                while self.chessboard[x - step][y + step] == 0 and (
                        self.queenMoveNegative[(x - step, y + step)] == 0 or self.queenMoveNegative[
                    (x - step, y + step)] > n):
                    self.queenMoveNegative[(x - step, y + step)] = n
                    nextCoord.append((x - step, y + step))
                    step += 1

                step = 1
                while self.chessboard[x][y - step] == 0 and (
                        self.queenMoveNegative[(x, y - step)] == 0 or self.queenMoveNegative[(x, y - step)] > n):
                    self.queenMoveNegative[(x, y - step)] = n
                    nextCoord.append((x, y - step))
                    step += 1
                step = 1
                while self.chessboard[x][y + step] == 0 and (
                        self.queenMoveNegative[(x, y + step)] == 0 or self.queenMoveNegative[(x, y + step)] > n):
                    self.queenMoveNegative[(x, y + step)] = n
                    nextCoord.append((x, y + step))
                    step += 1

                step = 1
                while self.chessboard[x + step][y - step] == 0 and (
                        self.queenMoveNegative[(x + step, y - step)] == 0 or self.queenMoveNegative[
                    (x + step, y - step)] > n):
                    self.queenMoveNegative[(x + step, y - step)] = n
                    nextCoord.append((x + step, y - step))
                    step += 1
                step = 1
                while self.chessboard[x + step][y] == 0 and (
                        self.queenMoveNegative[(x + step, y)] == 0 or self.queenMoveNegative[(x + step, y)] > n):
                    self.queenMoveNegative[(x + step, y)] = n
                    nextCoord.append((x + step, y))
                    step += 1
                step = 1
                while self.chessboard[x + step][y + step] == 0 and (
                        self.queenMoveNegative[(x + step, y + step)] == 0 or self.queenMoveNegative[
                    (x + step, y + step)] > n):
                    self.queenMoveNegative[(x + step, y + step)] = n
                    nextCoord.append((x + step, y + step))
                    step += 1

            NegativeCollect.clear()
            NegativeCollect = nextCoord[:]

    # 计算估值
    def computeValue(self):
        t1 = 0
        t2 = 0
        c1 = 0
        c2 = 0
        w = 0
        flag = 1 if self.status == 0 else -1
        for x in range(1, 11):
            for y in range(1, 11):
                if self.chessboard[x][y] == 0:
                    # 计算t1
                    if self.queenMovePositive[(x, y)] == self.queenMoveNegative[(x, y)]:
                        if self.queenMovePositive[(x, y)] != 0:
                            t1 += 0.1
                    elif self.queenMovePositive[(x, y)] < self.queenMoveNegative[(x, y)]:
                        if self.queenMovePositive[(x, y)] == 0:
                            t1 -= flag
                        else:
                            t1 += flag
                    else:
                        if self.queenMoveNegative[(x, y)] == 0:
                            t1 += flag
                        else:
                            t1 -= flag
                    # 计算t2
                    if self.kingMovePositive[(x, y)] == self.kingMoveNegative[(x, y)]:
                        if self.kingMovePositive[(x, y)] != 0:
                            t2 += 0.1
                    elif self.kingMovePositive[(x, y)] < self.kingMoveNegative[(x, y)]:
                        if self.kingMovePositive[(x, y)] == 0:
                            t2 -= flag
                        else:
                            t2 += flag
                    else:
                        if self.kingMoveNegative[(x, y)] == 0:
                            t2 += flag
                        else:
                            t2 -= flag
                    # 计算c1
                    if self.queenMovePositive[(x, y)] != 0 and self.queenMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            c1 += pow(2, -self.queenMovePositive[(x, y)]) - pow(2, -self.queenMoveNegative[(x, y)])
                        else:
                            c1 += pow(2, -self.queenMoveNegative[(x, y)]) - pow(2, -self.queenMovePositive[(x, y)])
                        # 计算w
                        w += pow(2, -fabs(self.queenMovePositive[(x, y)] - self.queenMoveNegative[(x, y)]))
                    elif self.queenMovePositive[(x, y)] == 0 and self.queenMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            c1 += 1 - pow(2, -self.queenMoveNegative[(x, y)])
                        else:
                            c1 += pow(2, -self.queenMoveNegative[(x, y)]) - 1
                    elif self.queenMovePositive[(x, y)] != 0 and self.queenMoveNegative[(x, y)] == 0:
                        if flag == 1:
                            c1 += pow(2, -self.queenMovePositive[(x, y)]) - 1
                        else:
                            c1 += 1 - pow(2, -self.queenMovePositive[(x, y)])
                    # 计算c2
                    if self.kingMovePositive[(x, y)] != 0 and self.kingMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            delta = (self.kingMovePositive[(x, y)] - self.kingMoveNegative[(x, y)]) / 6
                        else:
                            delta = (self.kingMoveNegative[(x, y)] - self.kingMovePositive[(x, y)]) / 6
                        c2 += min(1, max(-1, delta))
                    elif self.kingMovePositive[(x, y)] == 0 and self.kingMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            delta = - self.kingMoveNegative[(x, y)] / 6
                            c2 += max(-1, delta)
                        else:
                            delta = self.kingMoveNegative[(x, y)] / 6
                            c2 += min(1, delta)
                    elif self.kingMovePositive[(x, y)] != 0 and self.kingMoveNegative[(x, y)] == 0:
                        if flag == 1:
                            delta = self.kingMovePositive[(x, y)] / 6
                            c2 += min(1, delta)
                        else:
                            delta = -self.kingMovePositive[(x, y)] / 6
                            c2 += max(-1, delta)

        c1 *= 2
        # 此公式有待优化
        a = 5 / (w + 5)
        b = (w / (w + 20)) / 2
        c = (1 - (a + b)) / 4
        self.value = a * t1 + b * t2 + c * (c1 + c2)
        '''
        # 书上的公式
        if w>=0 and w<=1:
            self.value=t1
        elif w>1 and w<=45:
            self.value=0.3*(t1+t2)+0.2*(c1+c2)
        elif w>45 and w<=55:
            self.value=0.4*t2+0.3*(c1+c2)
        else:
            self.value=0.3*t2+0.3*c1+0.4*c2
        '''
