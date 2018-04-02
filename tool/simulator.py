# -*- coding: utf-8 -*-
# @create_time： 2018/3/11
# @move_time: 2018/3/13 from strategy to tool
# @author: RuiQing Chen
# @definition:

from random import choice, randrange
from copy import deepcopy


class Simulator:
    def __init__(self, chessboard, status, chess_coord, simulation_num):
        self.status = status
        self.simulation_num = simulation_num
        self.win_num = 0
        self.convert(chessboard,chess_coord)

    # 将二维数组转换为棋盘字典，以及列表坐标
    def convert(self,chessboard,chess_coord):
        self.chessboard={}
        for i in range(12):
            for j in range(12):
                self.chessboard[(i,j)]=chessboard[i][j]
        self.chess_coord=[]
        for i in range(2):
            temp=[]
            for j in range(0,7,2):
                temp.append(tuple([chess_coord[i][j],chess_coord[i][j+1]]))
            self.chess_coord.append(temp)

    # 棋子的随机移动
    def chessMove(self, chessboard, status, chess_coord):
        if status == 0:
            coord = chess_coord[0][:]
        else:
            coord = chess_coord[1][:]
        while len(coord):
            select_coord = choice(coord)
            direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            while len(direction):
                select_direct = choice(direction)
                x = select_coord[0]
                y = select_coord[1]
                if select_direct == (-1, -1):
                    step = 1
                    while chessboard[(x - step, y - step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x - d, y - d, chessboard)
                        return True
                    else:
                        direction.remove((-1, -1))
                elif select_direct == (-1, 0):
                    step = 1
                    while chessboard[(x - step, y)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x - d, y, chessboard)
                        return True
                    else:
                        direction.remove((-1, 0))
                elif select_direct == (-1, 1):
                    step = 1
                    while chessboard[(x - step, y + step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x - d, y + d, chessboard)
                        return True
                    else:
                        direction.remove((-1, 1))

                elif select_direct == (0, -1):
                    step = 1
                    while chessboard[(x, y - step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x, y - d, chessboard)
                        return True
                    else:
                        direction.remove((0, -1))
                elif select_direct == (0, 1):
                    step = 1
                    while chessboard[(x, y + step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x, y + d, chessboard)
                        return True
                    else:
                        direction.remove((0, 1))

                elif select_direct == (1, -1):
                    step = 1
                    while chessboard[(x + step, y - step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x + d, y - d, chessboard)
                        return True
                    else:
                        direction.remove((1, -1))
                elif select_direct == (1, 0):
                    step = 1
                    while chessboard[(x + step, y)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x + d, y, chessboard)
                        return True
                    else:
                        direction.remove((1, 0))
                else:
                    step = 1
                    while chessboard[(x + step, y + step)] == 0:
                        step += 1
                    if step > 1:
                        d = randrange(1, step)
                        self.arrowShoot(x, y, x + d, y + d, chessboard)
                        return True
                    else:
                        direction.remove((1, 1))
            coord.remove(select_coord)
        return False

    # 障碍的随机设置
    def arrowShoot(self, lx, ly, x, y, chessboard):
        chessboard[(x, y)] = chessboard[(lx, ly)]
        chessboard[(lx, ly)] = 0
        direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        while len(direction):
            select_direct = choice(direction)
            if select_direct == (-1, -1):
                step = 1
                while chessboard[(x - step, y - step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x - d, y - d]
                    break
                else:
                    direction.remove((-1, -1))
            elif select_direct == (-1, 0):
                step = 1
                while chessboard[(x - step, y)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x - d, y]
                    break
                else:
                    direction.remove((-1, 0))
            elif select_direct == (-1, 1):
                step = 1
                while chessboard[(x - step, y + step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x - d, y + d]
                    break
                else:
                    direction.remove((-1, 1))

            elif select_direct == (0, -1):
                step = 1
                while chessboard[(x, y - step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x, y - d]
                    break
                else:
                    direction.remove((0, -1))
            elif select_direct == (0, 1):
                step = 1
                while chessboard[(x, y + step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x, y + d]
                    break
                else:
                    direction.remove((0, 1))

            elif select_direct == (1, -1):
                step = 1
                while chessboard[(x + step, y - step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x + d, y - d]
                    break
                else:
                    direction.remove((1, -1))
            elif select_direct == (1, 0):
                step = 1
                while chessboard[(x + step, y)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x + d, y]
                    break
                else:
                    direction.remove((1, 0))
            else:
                step = 1
                while chessboard[(x + step, y + step)] == 0:
                    step += 1
                if step > 1:
                    d = randrange(1, step)
                    self.result=[lx, ly, x, y, x + d, y + d]
                    break
                else:
                    direction.remove((1, 1))

        chessboard[(lx, ly)] = chessboard[(x, y)]
        chessboard[(x, y)] = 0

    # 游戏模拟
    def simulate(self):
        try:
            for i in range(self.simulation_num):
                chessboard = deepcopy(self.chessboard)
                chess_coord = self.chess_coord[:]
                status = self.status
                while self.chessMove(chessboard, status, chess_coord):
                    chessboard[(self.result[2], self.result[3])] = chessboard[(self.result[0], self.result[1])]
                    chessboard[(self.result[0], self.result[1])] = 0
                    chessboard[(self.result[4], self.result[5])] = 1
                    if status == False:
                        chess_coord[0].remove((self.result[0], self.result[1]))
                        chess_coord[0].append((self.result[2], self.result[3]))
                        status = True
                    else:
                        chess_coord[1].remove((self.result[0], self.result[1]))
                        chess_coord[1].append((self.result[2], self.result[3]))
                        status = False
                if status != self.status:
                    self.win_num += 1
        except Exception as e:
            print(e)
