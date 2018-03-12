# -*- coding: utf-8 -*-
'''
@time： 2018/3/9
@author: RuiQing Chen
@definition:
'''
from copy import deepcopy


class startegy():
    def __init__(self, chessbroad, status, valuecoord):
        self.chessbroad = deepcopy(chessbroad)
        self.broadChange()
        self.status = status
        self.valuecoord = valuecoord[:]

    # 棋盘外加保护边界用于估值以及走法生成
    def broadChange(self):
        for i, j in zip([0] * 10, range(11)):
            self.chessbroad[(i, j)] = 1
            self.chessbroad[(11 - i, 11 - j)] = 1
            self.chessbroad[(j, 11)] = 1
            self.chessbroad[(11 - j, 0)] = 1
