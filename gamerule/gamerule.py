# -*- coding: utf-8 -*-
# @time： 2018/3/3
# @author: RuiQing Chen
# @definition:winner: 0——正方胜  1——反方胜  -1——胜负未知
#             over: true——游戏结束  false——游戏未结束

from copy import deepcopy


class GameRule:
    def __init__(self):
        self.winner = -1
        self.over = False
        self.blank = 0

    # 判断走法是否合理
    def moveRule(self, coord, last_x, last_y, curr_x, curr_y):
        delta_x = curr_x - last_x
        flag_x = 1 if delta_x > 0 else -1
        delta_y = curr_y - last_y
        flag_y = 1 if delta_y > 0 else -1
        last_sub = last_y - last_x
        last_add = last_y + last_x
        if last_x == curr_x:
            for i in range(last_y + flag_y, curr_y + flag_y, flag_y):
                if coord[(last_x, i)] == 1 or coord[(last_x, i)] == 2 or coord[(last_x, i)] == 3:
                    return False
        elif last_y == curr_y:
            for i in range(last_x + flag_x, curr_x + flag_x, flag_x):
                if coord[(i, last_y)] == 1 or coord[(i, last_y)] == 2 or coord[(i, last_y)] == 3:
                    return False
        elif delta_x == delta_y:
            for i in range(last_x + flag_x, curr_x + flag_x, flag_x):
                if coord[(i, i + last_sub)] == 1 or coord[(i, i + last_sub)] == 2 or coord[(i, i + last_sub)] == 3:
                    return False
        elif delta_x == -delta_y:
            for i in range(last_x + flag_x, curr_x + flag_x, flag_x):
                if coord[(i, last_add - i)] == 1 or coord[(i, last_add - i)] == 2 or coord[(i, last_add - i)] == 3:
                    return False
        else:
            return False
        return True

    # 判断棋局是否结束
    def isOver(self, coord, turn, chess_coord):
        count = 0
        count1 = 0
        for value in chess_coord[0]:
            x = value[0]
            y = value[1]
            if (x - 1 == 0 or y - 1 == 0 or coord[(x - 1, y - 1)] != 0) and (
                    x - 1 == 0 or coord[(x - 1, y)] != 0) and \
                    (y - 1 == 0 or coord[(x, y - 1)] != 0) and (
                    x - 1 == 0 or y + 1 == 11 or coord[(x - 1, y + 1)] != 0) and \
                    (x + 1 == 11 or y - 1 == 0 or coord[(x + 1, y - 1)] != 0) and (
                    x + 1 == 11 or coord[(x + 1, y)] != 0) and \
                    (y + 1 == 11 or coord[(x, y + 1)] != 0) and (
                    x + 1 == 11 or y + 1 == 11 or coord[(x + 1, y + 1)] != 0):
                count += 1
        for value in chess_coord[1]:
            x = value[0]
            y = value[1]
            if (x - 1 == 0 or y - 1 == 0 or coord[(x - 1, y - 1)] != 0) and (
                    x - 1 == 0 or coord[(x - 1, y)] != 0) and \
                    (y - 1 == 0 or coord[(x, y - 1)] != 0) and (
                    x - 1 == 0 or y + 1 == 11 or coord[(x - 1, y + 1)] != 0) and \
                    (x + 1 == 11 or y - 1 == 0 or coord[(x + 1, y - 1)] != 0) and (
                    x + 1 == 11 or coord[(x + 1, y)] != 0) and \
                    (y + 1 == 11 or coord[(x, y + 1)] != 0) and (
                    x + 1 == 11 or y + 1 == 11 or coord[(x + 1, y + 1)] != 0):
                count1 += 1
        if count == 4:
            if count1 == 4:
                if turn == 3 or turn == 1:
                    self.winner = 0
                else:
                    self.winner = 1
            else:
                self.winner = 1
            self.over = True
        else:
            if count1 == 4:
                self.winner = 0
                self.over = True
            else:
                self.over = False
        if self.over==True:
            self.checkBlank(coord, turn, chess_coord)

    def checkBlank(self, coord, turn, chess_coord):
        chessboard = deepcopy(coord)
        for i, j in zip([0] * 11, range(11)):
            chessboard[(i, j)] = 1
            chessboard[(11 - i, 11 - j)] = 1
            chessboard[(j, 11)] = 1
            chessboard[(11 - j, 0)] = 1
        self.blank = 0
        if turn == 3 or turn == 1:
            flag = 0
        else:
            flag = 1
        for value in chess_coord[flag]:
            x = value[0]
            y = value[1]
            step = 1
            while coord[(x - step, y - step)] == 0:
                self.blank += 1
                step += 1
            step = 1
            while coord[(x - step, y )] == 0:
                self.blank += 1
                step += 1
            step = 1
            while coord[(x - step, y + step)] == 0:
                self.blank += 1
                step += 1

            step = 1
            while coord[(x , y - step)] == 0:
                self.blank += 1
                step += 1
            step = 1
            while coord[(x , y + step)] == 0:
                self.blank += 1
                step += 1

            step = 1
            while coord[(x + step, y - step)] == 0:
                self.blank += 1
                step += 1
            step = 1
            while coord[(x + step, y )] == 0:
                self.blank += 1
                step += 1
            step = 1
            while coord[(x + step, y + step)] == 0:
                self.blank += 1
                step += 1
