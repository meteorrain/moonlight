# -*- coding: utf-8 -*-
'''
@time： 2018/3/3
@author: RuiQing Chen
@definition:winner: 0——正方胜  1——反方胜  -1——胜负未知
            over: true——游戏结束  false——游戏未结束
'''


class gameRule():
    def __init__(self):
        self.winner = -1
        self.over = False

    # 判断走法是否合理
    def moveRule(self, coord, lastx, lasty, currentx, currenty):
        dvaluex = currentx - lastx
        flagx = 1 if dvaluex > 0 else -1
        dvaluey = currenty - lasty
        flagy = 1 if dvaluey > 0 else -1
        dlast = lasty - lastx
        slast = lasty + lastx
        if lastx == currentx:
            for i in range(lasty + flagy, currenty + flagy, flagy):
                if coord[(lastx, i)] == 1 or coord[(lastx, i)] == 2 or coord[(lastx, i)] == 3:
                    return False
        elif lasty == currenty:
            for i in range(lastx + flagx, currentx + flagx, flagx):
                if coord[(i, lasty)] == 1 or coord[(i, lasty)] == 2 or coord[(i, lasty)] == 3:
                    return False
        elif dvaluex == dvaluey:
            for i in range(lastx + flagx, currentx + flagx, flagx):
                if coord[(i, i + dlast)] == 1 or coord[(i, i + dlast)] == 2 or coord[(i, i + dlast)] == 3:
                    return False
        elif dvaluex == -dvaluey:
            for i in range(lastx + flagx, currentx + flagx, flagx):
                if coord[(i, slast - i)] == 1 or coord[(i, slast - i)] == 2 or coord[(i, slast - i)] == 3:
                    return False
        else:
            return False
        return True

    # 判断棋局是否结束
    def isOver(self, coord, turn):
        count = 0
        if turn == 1 or turn == 3:
            for x in range(1, 11):
                for y in range(1, 11):
                    if (coord[(x, y)] == 2):
                        if (x - 1 == 0 or y - 1 == 0 or coord[(x - 1, y - 1)] != 0) and (
                                x - 1 == 0 or coord[(x - 1, y)] != 0) and \
                                (y - 1 == 0 or coord[(x, y - 1)] != 0) and (
                                x - 1 == 0 or y + 1 == 11 or coord[(x - 1, y + 1)] != 0) and \
                                (x + 1 == 11 or y - 1 == 0 or coord[(x + 1, y - 1)] != 0) and (
                                x + 1 == 11 or coord[(x + 1, y)] != 0) and \
                                (y + 1 == 11 or coord[(x, y + 1)] != 0) and (
                                x + 1 == 11 or y + 1 == 11 or coord[(x + 1, y + 1)] != 0):
                            count += 1
            if count == 4:
                self.winner = 1
                self.over = True
        else:
            for x in range(1, 11):
                for y in range(1, 11):
                    if (coord[(x, y)] == 3):
                        if (x - 1 == 0 or y - 1 == 0 or coord[(x - 1, y - 1)] != 0) and (
                                x - 1 == 0 or coord[(x - 1, y)] != 0) and \
                                (y - 1 == 0 or coord[(x, y - 1)] != 0) and (
                                x - 1 == 0 or y + 1 == 11 or coord[(x - 1, y + 1)] != 0) and \
                                (x + 1 == 11 or y - 1 == 0 or coord[(x + 1, y - 1)] != 0) and (
                                x + 1 == 11 or coord[(x + 1, y)] != 0) and \
                                (y + 1 == 11 or coord[(x, y + 1)] != 0) and (
                                x + 1 == 11 or y + 1 == 11 or coord[(x + 1, y + 1)] != 0):
                            count += 1
            if count == 4:
                self.winner = 0
                self.over = True
