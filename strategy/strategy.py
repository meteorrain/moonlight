# -*- coding: utf-8 -*-
# @time： 2018/3/9
# @author: RuiQing Chen
# @definition:

from copy import deepcopy


class Strategy:
    def __init__(self, chessboard, status, chess_coord):
        self.chessboard = deepcopy(chessboard)
        self.broadChange()
        self.status = status
        self.chess_coord = chess_coord[:]

    # 棋盘外加保护边界用于估值以及走法生成
    def broadChange(self):
        for i, j in zip([0] * 10, range(11)):
            self.chessboard[(i, j)] = 1
            self.chessboard[(11 - i, 11 - j)] = 1
            self.chessboard[(j, 11)] = 1
            self.chessboard[(11 - j, 0)] = 1
