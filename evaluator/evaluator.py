# -*- coding: utf-8 -*-
'''
@time： 2018/3/9
@author: RuiQing Chen
@definition:
'''
from math import fabs


class evaluator():
    def __init__(self, chessbroad, status, valuecoord):
        self.chessbroad = chessbroad
        self.status = status
        self.valuecoord = valuecoord
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
        for coord in self.valuecoord[0]:
            if self.chessbroad[(coord[0] - 1, coord[1] - 1)] == 0 and self.kingMovePositive[
                (coord[0] - 1, coord[1] - 1)] == 0:
                self.kingMovePositive[(coord[0] - 1, coord[1] - 1)] = 1
                PositiveCollect.append((coord[0] - 1, coord[1] - 1))
            if self.chessbroad[(coord[0] - 1, coord[1])] == 0 and self.kingMovePositive[(coord[0] - 1, coord[1])] == 0:
                self.kingMovePositive[(coord[0] - 1, coord[1])] = 1
                PositiveCollect.append((coord[0] - 1, coord[1]))
            if self.chessbroad[(coord[0] - 1, coord[1] + 1)] == 0 and self.kingMovePositive[
                (coord[0] - 1, coord[1] + 1)] == 0:
                self.kingMovePositive[(coord[0] - 1, coord[1] + 1)] = 1
                PositiveCollect.append((coord[0] - 1, coord[1] + 1))

            if self.chessbroad[(coord[0], coord[1] - 1)] == 0 and self.kingMovePositive[(coord[0], coord[1] - 1)] == 0:
                self.kingMovePositive[(coord[0], coord[1] - 1)] = 1
                PositiveCollect.append((coord[0], coord[1] - 1))
            if self.chessbroad[(coord[0], coord[1] + 1)] == 0 and self.kingMovePositive[(coord[0], coord[1] + 1)] == 0:
                self.kingMovePositive[(coord[0], coord[1] + 1)] = 1
                PositiveCollect.append((coord[0], coord[1] + 1))

            if self.chessbroad[(coord[0] + 1, coord[1] - 1)] == 0 and self.kingMovePositive[
                (coord[0] + 1, coord[1] - 1)] == 0:
                self.kingMovePositive[(coord[0] + 1, coord[1] - 1)] = 1
                PositiveCollect.append((coord[0] + 1, coord[1] - 1))
            if self.chessbroad[(coord[0] + 1, coord[1])] == 0 and self.kingMovePositive[(coord[0] + 1, coord[1])] == 0:
                self.kingMovePositive[(coord[0] + 1, coord[1])] = 1
                PositiveCollect.append((coord[0] + 1, coord[1]))
            if self.chessbroad[(coord[0] + 1, coord[1] + 1)] == 0 and self.kingMovePositive[
                (coord[0] + 1, coord[1] + 1)] == 0:
                self.kingMovePositive[(coord[0] + 1, coord[1] + 1)] = 1
                PositiveCollect.append((coord[0] + 1, coord[1] + 1))

        for coord in self.valuecoord[1]:
            if self.chessbroad[(coord[0] - 1, coord[1] - 1)] == 0 and self.kingMoveNegative[
                (coord[0] - 1, coord[1] - 1)] == 0:
                self.kingMoveNegative[(coord[0] - 1, coord[1] - 1)] = 1
                NegativeCollect.append((coord[0] - 1, coord[1] - 1))
            if self.chessbroad[(coord[0] - 1, coord[1])] == 0 and self.kingMoveNegative[(coord[0] - 1, coord[1])] == 0:
                self.kingMoveNegative[(coord[0] - 1, coord[1])] = 1
                NegativeCollect.append((coord[0] - 1, coord[1]))
            if self.chessbroad[(coord[0] - 1, coord[1] + 1)] == 0 and self.kingMoveNegative[
                (coord[0] - 1, coord[1] + 1)] == 0:
                self.kingMoveNegative[(coord[0] - 1, coord[1] + 1)] = 1
                NegativeCollect.append((coord[0] - 1, coord[1] + 1))

            if self.chessbroad[(coord[0], coord[1] - 1)] == 0 and self.kingMoveNegative[(coord[0], coord[1] - 1)] == 0:
                self.kingMoveNegative[(coord[0], coord[1] - 1)] = 1
                NegativeCollect.append((coord[0], coord[1] - 1))
            if self.chessbroad[(coord[0], coord[1] + 1)] == 0 and self.kingMoveNegative[(coord[0], coord[1] + 1)] == 0:
                self.kingMoveNegative[(coord[0], coord[1] + 1)] = 1
                NegativeCollect.append((coord[0], coord[1] + 1))

            if self.chessbroad[(coord[0] + 1, coord[1] - 1)] == 0 and self.kingMoveNegative[
                (coord[0] + 1, coord[1] - 1)] == 0:
                self.kingMoveNegative[(coord[0] + 1, coord[1] - 1)] = 1
                NegativeCollect.append((coord[0] + 1, coord[1] - 1))
            if self.chessbroad[(coord[0] + 1, coord[1])] == 0 and self.kingMoveNegative[(coord[0] + 1, coord[1])] == 0:
                self.kingMoveNegative[(coord[0] + 1, coord[1])] = 1
                NegativeCollect.append((coord[0] + 1, coord[1]))
            if self.chessbroad[(coord[0] + 1, coord[1] + 1)] == 0 and self.kingMoveNegative[
                (coord[0] + 1, coord[1] + 1)] == 0:
                self.kingMoveNegative[(coord[0] + 1, coord[1] + 1)] = 1
                NegativeCollect.append((coord[0] + 1, coord[1] + 1))
        nextCoord = []
        for n in range(2, 9):
            nextCoord.clear()
            for coord in PositiveCollect:
                if self.chessbroad[(coord[0] - 1, coord[1] - 1)] == 0 and (
                        self.kingMovePositive[(coord[0] - 1, coord[1] - 1)] > n or
                        self.kingMovePositive[(coord[0] - 1, coord[1] - 1)] == 0):
                    nextCoord.append((coord[0] - 1, coord[1] - 1))
                    self.kingMovePositive[(coord[0] - 1, coord[1] - 1)] = n
                if self.chessbroad[(coord[0] - 1, coord[1])] == 0 and (
                        self.kingMovePositive[(coord[0] - 1, coord[1])] > n or
                        self.kingMovePositive[(coord[0] - 1, coord[1])] == 0):
                    nextCoord.append((coord[0] - 1, coord[1]))
                    self.kingMovePositive[(coord[0] - 1, coord[1])] = n
                if self.chessbroad[(coord[0] - 1, coord[1] + 1)] == 0 and (
                        self.kingMovePositive[(coord[0] - 1, coord[1] + 1)] > n or
                        self.kingMovePositive[(coord[0] - 1, coord[1] + 1)] == 0):
                    nextCoord.append((coord[0] - 1, coord[1] + 1))
                    self.kingMovePositive[(coord[0] - 1, coord[1] + 1)] = n

                if self.chessbroad[(coord[0], coord[1] - 1)] == 0 and (
                        self.kingMovePositive[(coord[0], coord[1] - 1)] > n or
                        self.kingMovePositive[(coord[0], coord[1] - 1)] == 0):
                    nextCoord.append((coord[0], coord[1] - 1))
                    self.kingMovePositive[(coord[0], coord[1] - 1)] = n
                if self.chessbroad[(coord[0], coord[1] + 1)] == 0 and (
                        self.kingMovePositive[(coord[0], coord[1] + 1)] > n or
                        self.kingMovePositive[(coord[0], coord[1] + 1)] == 0):
                    nextCoord.append((coord[0], coord[1] + 1))
                    self.kingMovePositive[(coord[0], coord[1] + 1)] = n

                if self.chessbroad[(coord[0] + 1, coord[1] - 1)] == 0 and (
                        self.kingMovePositive[(coord[0] + 1, coord[1] - 1)] > n or
                        self.kingMovePositive[(coord[0] + 1, coord[1] - 1)] == 0):
                    nextCoord.append((coord[0] + 1, coord[1] - 1))
                    self.kingMovePositive[(coord[0] + 1, coord[1] - 1)] = n
                if self.chessbroad[(coord[0] + 1, coord[1])] == 0 and (
                        self.kingMovePositive[(coord[0] + 1, coord[1])] > n or
                        self.kingMovePositive[(coord[0] + 1, coord[1])] == 0):
                    nextCoord.append((coord[0] + 1, coord[1]))
                    self.kingMovePositive[(coord[0] + 1, coord[1])] = n
                if self.chessbroad[(coord[0] + 1, coord[1] + 1)] == 0 and (
                        self.kingMovePositive[(coord[0] + 1, coord[1] + 1)] > n or
                        self.kingMovePositive[(coord[0] + 1, coord[1] + 1)] == 0):
                    nextCoord.append((coord[0] + 1, coord[1] + 1))
                    self.kingMovePositive[(coord[0] + 1, coord[1] + 1)] = n
            PositiveCollect.clear()
            PositiveCollect = nextCoord[:]
            nextCoord.clear()
            for coord in NegativeCollect:
                if self.chessbroad[(coord[0] - 1, coord[1] - 1)] == 0 and (
                        self.kingMoveNegative[(coord[0] - 1, coord[1] - 1)] > n or
                        self.kingMoveNegative[(coord[0] - 1, coord[1] - 1)] == 0):
                    nextCoord.append((coord[0] - 1, coord[1] - 1))
                    self.kingMoveNegative[(coord[0] - 1, coord[1] - 1)] = n
                if self.chessbroad[(coord[0] - 1, coord[1])] == 0 and (
                        self.kingMoveNegative[(coord[0] - 1, coord[1])] > n or
                        self.kingMoveNegative[(coord[0] - 1, coord[1])] == 0):
                    nextCoord.append((coord[0] - 1, coord[1]))
                    self.kingMoveNegative[(coord[0] - 1, coord[1])] = n
                if self.chessbroad[(coord[0] - 1, coord[1] + 1)] == 0 and (
                        self.kingMoveNegative[(coord[0] - 1, coord[1] + 1)] > n or
                        self.kingMoveNegative[(coord[0] - 1, coord[1] + 1)] == 0):
                    nextCoord.append((coord[0] - 1, coord[1] + 1))
                    self.kingMoveNegative[(coord[0] - 1, coord[1] + 1)] = n

                if self.chessbroad[(coord[0], coord[1] - 1)] == 0 and (
                        self.kingMoveNegative[(coord[0], coord[1] - 1)] > n or
                        self.kingMoveNegative[(coord[0], coord[1] - 1)] == 0):
                    nextCoord.append((coord[0], coord[1] - 1))
                    self.kingMoveNegative[(coord[0], coord[1] - 1)] = n
                if self.chessbroad[(coord[0], coord[1] + 1)] == 0 and (
                        self.kingMoveNegative[(coord[0], coord[1] + 1)] > n or
                        self.kingMoveNegative[(coord[0], coord[1] + 1)] == 0):
                    nextCoord.append((coord[0], coord[1] + 1))
                    self.kingMoveNegative[(coord[0], coord[1] + 1)] = n

                if self.chessbroad[(coord[0] + 1, coord[1] - 1)] == 0 and (
                        self.kingMoveNegative[(coord[0] + 1, coord[1] - 1)] > n or
                        self.kingMoveNegative[(coord[0] + 1, coord[1] - 1)] == 0):
                    nextCoord.append((coord[0] + 1, coord[1] - 1))
                    self.kingMoveNegative[(coord[0] + 1, coord[1] - 1)] = n
                if self.chessbroad[(coord[0] + 1, coord[1])] == 0 and (
                        self.kingMoveNegative[(coord[0] + 1, coord[1])] > n or
                        self.kingMoveNegative[(coord[0] + 1, coord[1])] == 0):
                    nextCoord.append((coord[0] + 1, coord[1]))
                    self.kingMoveNegative[(coord[0] + 1, coord[1])] = n
                if self.chessbroad[(coord[0] + 1, coord[1] + 1)] == 0 and (
                        self.kingMoveNegative[(coord[0] + 1, coord[1] + 1)] > n or
                        self.kingMoveNegative[(coord[0] + 1, coord[1] + 1)] == 0):
                    nextCoord.append((coord[0] + 1, coord[1] + 1))
                    self.kingMoveNegative[(coord[0] + 1, coord[1] + 1)] = n
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
        for coord in self.valuecoord[0]:
            x = coord[0]
            y = coord[1]
            step = 1
            while self.chessbroad[(x - step, y - step)] == 0:
                if self.queenMovePositive[(x - step, y - step)] == 0:
                    self.queenMovePositive[(x - step, y - step)] = 1
                    PositiveCollect.append((x - step, y - step))
                step += 1
            step = 1
            while self.chessbroad[(x - step, y)] == 0:
                if self.queenMovePositive[(x - step, y)] == 0:
                    self.queenMovePositive[(x - step, y)] = 1
                    PositiveCollect.append((x - step, y))
                step += 1
            step = 1
            while self.chessbroad[(x - step, y + step)] == 0:
                if self.queenMovePositive[(x - step, y + step)] == 0:
                    self.queenMovePositive[(x - step, y + step)] = 1
                    PositiveCollect.append((x - step, y + step))
                step += 1

            step = 1
            while self.chessbroad[(x, y - step)] == 0:
                if self.queenMovePositive[(x, y - step)] == 0:
                    self.queenMovePositive[(x, y - step)] = 1
                    PositiveCollect.append((x, y - step))
                step += 1
            step = 1
            while self.chessbroad[(x, y + step)] == 0:
                if self.queenMovePositive[(x, y + step)] == 0:
                    self.queenMovePositive[(x, y + step)] = 1
                    PositiveCollect.append((x, y + step))
                step += 1

            step = 1
            while self.chessbroad[(x + step, y - step)] == 0:
                if self.queenMovePositive[(x + step, y - step)] == 0:
                    self.queenMovePositive[(x + step, y - step)] = 1
                    PositiveCollect.append((x + step, y - step))
                step += 1
            step = 1
            while self.chessbroad[(x + step, y)] == 0:
                if self.queenMovePositive[(x + step, y)] == 0:
                    self.queenMovePositive[(x + step, y)] = 1
                    PositiveCollect.append((x + step, y))
                step += 1
            step = 1
            while self.chessbroad[(x + step, y + step)] == 0:
                if self.queenMovePositive[(x + step, y + step)] == 0:
                    self.queenMovePositive[(x + step, y + step)] = 1
                    PositiveCollect.append((x + step, y + step))
                step += 1

        for coord in self.valuecoord[1]:
            x = coord[0]
            y = coord[1]
            step = 1
            while self.chessbroad[(x - step, y - step)] == 0:
                if self.queenMoveNegative[(x - step, y - step)] == 0:
                    self.queenMoveNegative[(x - step, y - step)] = 1
                    NegativeCollect.append((x - step, y - step))
                step += 1
            step = 1
            while self.chessbroad[(x - step, y)] == 0:
                if self.queenMoveNegative[(x - step, y)] == 0:
                    self.queenMoveNegative[(x - step, y)] = 1
                    NegativeCollect.append((x - step, y))
                step += 1
            step = 1
            while self.chessbroad[(x - step, y + step)] == 0:
                if self.queenMoveNegative[(x - step, y + step)] == 0:
                    self.queenMoveNegative[(x - step, y + step)] = 1
                    NegativeCollect.append((x - step, y + step))
                step += 1

            step = 1
            while self.chessbroad[(x, y - step)] == 0:
                if self.queenMoveNegative[(x, y - step)] == 0:
                    self.queenMoveNegative[(x, y - step)] = 1
                    NegativeCollect.append((x, y - step))
                step += 1
            step = 1
            while self.chessbroad[(x, y + step)] == 0:
                if self.queenMoveNegative[(x, y + step)] == 0:
                    self.queenMoveNegative[(x, y + step)] = 1
                    NegativeCollect.append((x, y + step))
                step += 1

            step = 1
            while self.chessbroad[(x + step, y - step)] == 0:
                if self.queenMoveNegative[(x + step, y - step)] == 0:
                    self.queenMoveNegative[(x + step, y - step)] = 1
                    NegativeCollect.append((x + step, y - step))
                step += 1
            step = 1
            while self.chessbroad[(x + step, y)] == 0:
                if self.queenMoveNegative[(x + step, y)] == 0:
                    self.queenMoveNegative[(x + step, y)] = 1
                    NegativeCollect.append((x + step, y))
                step += 1
            step = 1
            while self.chessbroad[(x + step, y + step)] == 0:
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
                while self.chessbroad[(x - step, y - step)] == 0 and (
                        self.queenMovePositive[(x - step, y - step)] == 0 or self.queenMovePositive[
                    (x - step, y - step)] > n):
                    self.queenMovePositive[(x - step, y - step)] = n
                    nextCoord.append((x - step, y - step))
                    step += 1
                step = 1
                while self.chessbroad[(x - step, y)] == 0 and (
                        self.queenMovePositive[(x - step, y)] == 0 or self.queenMovePositive[(x - step, y)] > n):
                    self.queenMovePositive[(x - step, y)] = n
                    nextCoord.append((x - step, y))
                    step += 1
                step = 1
                while self.chessbroad[(x - step, y + step)] == 0 and (
                        self.queenMovePositive[(x - step, y + step)] == 0 or self.queenMovePositive[
                    (x - step, y + step)] > n):
                    self.queenMovePositive[(x - step, y + step)] = n
                    nextCoord.append((x - step, y + step))
                    step += 1

                step = 1
                while self.chessbroad[(x, y - step)] == 0 and (
                        self.queenMovePositive[(x, y - step)] == 0 or self.queenMovePositive[(x, y - step)] > n):
                    self.queenMovePositive[(x, y - step)] = n
                    nextCoord.append((x, y - step))
                    step += 1
                step = 1
                while self.chessbroad[(x, y + step)] == 0 and (
                        self.queenMovePositive[(x, y + step)] == 0 or self.queenMovePositive[(x, y + step)] > n):
                    self.queenMovePositive[(x, y + step)] = n
                    nextCoord.append((x, y + step))
                    step += 1

                step = 1
                while self.chessbroad[(x + step, y - step)] == 0 and (
                        self.queenMovePositive[(x + step, y - step)] == 0 or self.queenMovePositive[
                    (x + step, y - step)] > n):
                    self.queenMovePositive[(x + step, y - step)] = n
                    nextCoord.append((x + step, y - step))
                    step += 1
                step = 1
                while self.chessbroad[(x + step, y)] == 0 and (
                        self.queenMovePositive[(x + step, y)] == 0 or self.queenMovePositive[(x + step, y)] > n):
                    self.queenMovePositive[(x + step, y)] = n
                    nextCoord.append((x + step, y))
                    step += 1
                step = 1
                while self.chessbroad[(x + step, y + step)] == 0 and (
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
                while self.chessbroad[(x - step, y - step)] == 0 and (
                        self.queenMoveNegative[(x - step, y - step)] == 0 or self.queenMoveNegative[
                    (x - step, y - step)] > n):
                    self.queenMoveNegative[(x - step, y - step)] = n
                    nextCoord.append((x - step, y - step))
                    step += 1
                step = 1
                while self.chessbroad[(x - step, y)] == 0 and (
                        self.queenMoveNegative[(x - step, y)] == 0 or self.queenMoveNegative[(x - step, y)] > n):
                    self.queenMoveNegative[(x - step, y)] = n
                    nextCoord.append((x - step, y))
                    step += 1
                step = 1
                while self.chessbroad[(x - step, y + step)] == 0 and (
                        self.queenMoveNegative[(x - step, y + step)] == 0 or self.queenMoveNegative[
                    (x - step, y + step)] > n):
                    self.queenMoveNegative[(x - step, y + step)] = n
                    nextCoord.append((x - step, y + step))
                    step += 1

                step = 1
                while self.chessbroad[(x, y - step)] == 0 and (
                        self.queenMoveNegative[(x, y - step)] == 0 or self.queenMoveNegative[(x, y - step)] > n):
                    self.queenMoveNegative[(x, y - step)] = n
                    nextCoord.append((x, y - step))
                    step += 1
                step = 1
                while self.chessbroad[(x, y + step)] == 0 and (
                        self.queenMoveNegative[(x, y + step)] == 0 or self.queenMoveNegative[(x, y + step)] > n):
                    self.queenMoveNegative[(x, y + step)] = n
                    nextCoord.append((x, y + step))
                    step += 1

                step = 1
                while self.chessbroad[(x + step, y - step)] == 0 and (
                        self.queenMoveNegative[(x + step, y - step)] == 0 or self.queenMoveNegative[
                    (x + step, y - step)] > n):
                    self.queenMoveNegative[(x + step, y - step)] = n
                    nextCoord.append((x + step, y - step))
                    step += 1
                step = 1
                while self.chessbroad[(x + step, y)] == 0 and (
                        self.queenMoveNegative[(x + step, y)] == 0 or self.queenMoveNegative[(x + step, y)] > n):
                    self.queenMoveNegative[(x + step, y)] = n
                    nextCoord.append((x + step, y))
                    step += 1
                step = 1
                while self.chessbroad[(x + step, y + step)] == 0 and (
                        self.queenMoveNegative[(x + step, y + step)] == 0 or self.queenMoveNegative[
                    (x + step, y + step)] > n):
                    self.queenMoveNegative[(x + step, y + step)] = n
                    nextCoord.append((x + step, y + step))
                    step += 1

            NegativeCollect.clear()
            NegativeCollect = nextCoord[:]

    # 计算估值
    def computeValue(self):
        self.t1 = 0
        self.t2 = 0
        self.c1 = 0
        self.c2 = 0
        self.w = 0
        flag = 1 if self.status == 3 else -1
        for x in range(1, 11):
            for y in range(1, 11):
                if self.chessbroad[(x, y)] == 0:
                    # 计算t1
                    if self.queenMovePositive[(x, y)] == self.queenMoveNegative[(x, y)]:
                        if self.queenMovePositive[(x, y)] != 0:
                            self.t1 += 0.1
                    elif self.queenMovePositive[(x, y)] < self.queenMoveNegative[(x, y)]:
                        if self.queenMovePositive[(x, y)] == 0:
                            self.t1 -= flag
                        else:
                            self.t1 += flag
                    else:
                        if self.queenMoveNegative[(x, y)] == 0:
                            self.t1 += flag
                        else:
                            self.t1 -= flag
                    # 计算t2
                    if self.kingMovePositive[(x, y)] == self.kingMoveNegative[(x, y)]:
                        if self.kingMovePositive[(x, y)] != 0:
                            self.t2 += 0.1
                    elif self.kingMovePositive[(x, y)] < self.kingMoveNegative[(x, y)]:
                        if self.kingMovePositive[(x, y)] == 0:
                            self.t2 -= flag
                        else:
                            self.t2 += flag
                    else:
                        if self.kingMoveNegative[(x, y)] == 0:
                            self.t2 += flag
                        else:
                            self.t2 -= flag
                    # 计算c1
                    if self.queenMovePositive[(x, y)] != 0 and self.queenMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            self.c1 += pow(2, -self.queenMovePositive[(x, y)]) - pow(2, -self.queenMoveNegative[(x, y)])
                        else:
                            self.c1 += pow(2, -self.queenMoveNegative[(x, y)]) - pow(2, -self.queenMovePositive[(x, y)])
                        # 计算w
                        self.w += pow(2, -fabs(self.queenMovePositive[(x, y)] - self.queenMoveNegative[(x, y)]))
                    elif self.queenMovePositive[(x, y)] == 0 and self.queenMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            self.c1 += 1 - pow(2, -self.queenMoveNegative[(x, y)])
                        else:
                            self.c1 += pow(2, -self.queenMoveNegative[(x, y)]) - 1
                    elif self.queenMovePositive[(x, y)] != 0 and self.queenMoveNegative[(x, y)] == 0:
                        if flag == 1:
                            self.c1 += pow(2, -self.queenMovePositive[(x, y)]) - 1
                        else:
                            self.c1 += 1 - pow(2, -self.queenMovePositive[(x, y)])
                    # 计算c2
                    if self.kingMovePositive[(x, y)] != 0 and self.kingMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            delta = (self.kingMovePositive[(x, y)] - self.kingMoveNegative[(x, y)]) / 6
                        else:
                            delta = (self.kingMoveNegative[(x, y)] - self.kingMovePositive[(x, y)]) / 6
                        self.c2 += min(1, max(-1, delta))
                    elif self.kingMovePositive[(x, y)] == 0 and self.kingMoveNegative[(x, y)] != 0:
                        if flag == 1:
                            delta = - self.kingMoveNegative[(x, y)] / 6
                            self.c2 += max(-1, delta)
                        else:
                            delta = self.kingMoveNegative[(x, y)] / 6
                            self.c2 += min(1, delta)
                    elif self.kingMovePositive[(x, y)] != 0 and self.kingMoveNegative[(x, y)] == 0:
                        if flag == 1:
                            delta = self.kingMovePositive[(x, y)] / 6
                            self.c2 += min(1, delta)
                        else:
                            delta = -self.kingMovePositive[(x, y)] / 6
                            self.c2 += max(-1, delta)

        self.c1 *= 2
        # 此公式有待优化
        a = 5 / (self.w + 5)
        b = (self.w / (self.w + 20)) / 2
        c = (1 - (a + b)) / 4
        self.value = a * self.t1 + b * self.t2 + c * (self.c1 + self.c2)
        '''
        # 书上的公式
        if self.w>=0 and self.w<=1:
            self.value=self.t1
        elif self.w>1 and self.w<=45:
            self.value=0.3*(self.t1+self.t2)+0.2*(self.c1+self.c2)
        elif self.w>45 and self.w<=55:
            self.value=0.4*self.t2+0.3*(self.c1+self.c2)
        else:
            self.value=0.3*self.t2+0.3*self.c1+0.4*self.c2
        '''
