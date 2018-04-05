# -*- coding: utf-8 -*-
# @time： 2018/4/4
# @author: RuiQing Chen
# @definition:
#
from movegenerator import Node


class MoveGenerator_first:
    def __init__(self, state_space, location, curr_num):
        self.chessboard = state_space[location].chessboard
        self.status = state_space[location].status
        self.chess_coord = state_space[location].chess_coord
        self.location = location
        self.curr_num = curr_num
        self.state_space = state_space

    # 收集所有的走法
    def collectAllMove(self):
        flag = self.status
        for i in range(0, 7, 2):
            x = self.chess_coord[flag][i]
            y = self.chess_coord[flag][i + 1]
            step = 1
            while self.chessboard[x - step][y - step] == 0:
                self.collectAllArrowLocation(x, y, x - step, y - step)
                step += 1
            step = 1
            while self.chessboard[x - step][y] == 0:
                self.collectAllArrowLocation(x, y, x - step, y)
                step += 1
            step = 1
            while self.chessboard[x - step][y + step] == 0:
                self.collectAllArrowLocation(x, y, x - step, y + step)
                step += 1

            step = 1
            while self.chessboard[x][y - step] == 0:
                self.collectAllArrowLocation(x, y, x, y - step)
                step += 1
            step = 1
            while self.chessboard[x][y + step] == 0:
                self.collectAllArrowLocation(x, y, x, y + step)
                step += 1

            step = 1
            while self.chessboard[x + step][y - step] == 0:
                self.collectAllArrowLocation(x, y, x + step, y - step)
                step += 1
            step = 1
            while self.chessboard[x + step][y] == 0:
                self.collectAllArrowLocation(x, y, x + step, y)
                step += 1
            step = 1
            while self.chessboard[x + step][y + step] == 0:
                self.collectAllArrowLocation(x, y, x + step, y + step)
                step += 1

    # 收集当前棋子移动下所有放置障碍的方法
    def collectAllArrowLocation(self, lx, ly, x, y):
        self.chessboard[x][y] = self.chessboard[lx][ly]
        self.chessboard[lx][ly] = 0
        step = 1
        while self.chessboard[x - step][y - step] == 0:
            self.expand(lx, ly, x, y, x - step, y - step)
            step += 1

        step = 1
        while self.chessboard[x - step][y] == 0:
            self.expand(lx, ly, x, y, x - step, y)
            step += 1

        step = 1
        while self.chessboard[x - step][y + step] == 0:
            self.expand(lx, ly, x, y, x - step, y + step)
            step += 1

        step = 1
        while self.chessboard[x][y - step] == 0:
            self.expand(lx, ly, x, y, x, y - step)
            step += 1

        step = 1
        while self.chessboard[x][y + step] == 0:
            self.expand(lx, ly, x, y, x, y + step)
            step += 1

        step = 1
        while self.chessboard[x + step][y - step] == 0:
            self.expand(lx, ly, x, y, x + step, y - step)
            step += 1
        step = 1
        while self.chessboard[x + step][y] == 0:
            self.expand(lx, ly, x, y, x + step, y)
            step += 1
        step = 1
        while self.chessboard[x + step][y + step] == 0:
            self.expand(lx, ly, x, y, x + step, y + step)
            step += 1

        self.chessboard[lx][ly] = self.chessboard[x][y]
        self.chessboard[x][y] = 0

    def expand(self, last_x, last_y, x, y, arr_x, arr_y):
        node = self.state_space[self.location]
        print(self.curr_num.value)
        node.children[node.children_num] = self.curr_num
        self.state_space[self.curr_num.value] = Node(self.curr_num, 1 - node.status, 0, 0, 0.0, node.blank - 1,
                                                     False,
                                                     node.chessboard, node.chess_coord, node.id, child_num=0,
                                                     move=(last_x, last_y, x, y, arr_x, arr_y))
        self.curr_num.value += 1
        node.children_num += 1
