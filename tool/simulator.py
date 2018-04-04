# -*- coding: utf-8 -*-
# @create_time： 2018/3/11
# @move_time: 2018/3/13 from strategy to tool
# @author: RuiQing Chen
# @definition:

from random import choice, randrange
from copy import deepcopy
from ctypes import c_int
from time import time


class Simulator:
    def __init__(self, chessboard, status, chess_coord, simulation_num):
        self.status = status
        self.simulation_num = simulation_num
        self.win_num = 0
        # self.chessboard=chessboard
        # self.chess_coord=chess_coord
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
        coord_num=4
        # t1=time()
        while coord_num:
            select_coord = choice(coord)
            x = select_coord[0]
            y = select_coord[1]
            direction = []
            for i,j in zip([-1,-1,-1,0,0,1,1,1],[-1,0,1,-1,1,-1,0,1]):
                if chessboard[(x+i,y+j)]==0:
                    direction.append((i,j))
            if len(direction)==0:
                coord.remove(select_coord)
                coord_num-=1
            else:
                # t2=time()
                select_direct = choice(direction)
                if select_direct == (-1, -1):
                    step = 1
                    while chessboard[(x - step, y - step)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x - d, y - d, chessboard)

                elif select_direct == (-1, 0):
                    step = 1
                    while chessboard[(x - step, y)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x - d, y, chessboard)

                elif select_direct == (-1, 1):
                    step = 1
                    while chessboard[(x - step, y + step)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x - d, y + d, chessboard)


                elif select_direct == (0, -1):
                    step = 1
                    while chessboard[(x, y - step)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x, y - d, chessboard)

                elif select_direct == (0, 1):
                    step = 1
                    while chessboard[(x, y + step)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x, y + d, chessboard)


                elif select_direct == (1, -1):
                    step = 1
                    while chessboard[(x + step, y - step)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x + d, y - d, chessboard)

                elif select_direct == (1, 0):
                    step = 1
                    while chessboard[(x + step, y)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x + d, y, chessboard)

                elif select_direct == (1, 1):
                    step = 1
                    while chessboard[(x + step, y + step)] == 0:
                        step += 1
                    d = randrange(1, step)
                    self.arrowShoot(x, y, x + d, y + d, chessboard)

                # t3 = time()
                # print("小循环%.20f" % (t3 - t2))
                return True


        # t4=time()
        # print("大循环%.20f"%(t4-t1))
        return False

    # 障碍的随机设置
    def arrowShoot(self, lx, ly, x, y, chessboard):
        # t1=time()
        chessboard[(x, y)] = chessboard[(lx, ly)]
        chessboard[(lx, ly)] = 0
        direction = []
        for i, j in zip([-1, -1, -1, 0, 0, 1, 1, 1], [-1, 0, 1, -1, 1, -1, 0, 1]):
            if chessboard[(x + i, y + j)] == 0:
                direction.append((i, j))

        select_direct = choice(direction)
        if select_direct == (-1, -1):
            step = 1
            while chessboard[(x - step, y - step)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x - d, y - d]

        elif select_direct == (-1, 0):
            step = 1
            while chessboard[(x - step, y)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x - d, y]

        elif select_direct == (-1, 1):
            step = 1
            while chessboard[(x - step, y + step)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x - d, y + d]


        elif select_direct == (0, -1):
            step = 1
            while chessboard[(x, y - step)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x, y - d]

        elif select_direct == (0, 1):
            step = 1
            while chessboard[(x, y + step)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x, y + d]


        elif select_direct == (1, -1):
            step = 1
            while chessboard[(x + step, y - step)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x + d, y - d]

        elif select_direct == (1, 0):
            step = 1
            while chessboard[(x + step, y)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x + d, y]

        elif select_direct == (1, 1):
            step = 1
            while chessboard[(x + step, y + step)] == 0:
                step += 1
            d = randrange(1, step)
            self.result=[lx, ly, x, y, x + d, y + d]

        chessboard[(lx, ly)] = chessboard[(x, y)]
        chessboard[(x, y)] = 0
        # t2=time()
        # print("内循环%.20f"%(t2-t1))

    # 游戏模拟
    def simulate(self):
        try:
            for i in range(self.simulation_num):
                chessboard = deepcopy(self.chessboard)
                chess_coord = self.chess_coord[:]
                status = self.status
                # t1=time()
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

                # t2 = time()
                # print("模拟一趟的时间%f"%(t2-t1))
                if status != self.status:
                    self.win_num += 1
        except Exception as e:
            print(e)

if __name__=='__main__':
    chessboard={}
    chess_coord=[[],[]]
    for x in range(1, 11):
        for y in range(1, 11):
            if x == 1 and y == 4 or x == 4 and y == 1 or x == 7 and y == 1 or x == 10 and y == 4:
                chessboard[(x, y)] = 2
                chess_coord[0].append((x, y))
            elif x == 1 and y == 7 or x == 4 and y == 10 or x == 7 and y == 10 or x == 10 and y == 7:
                chessboard[(x, y)] = 3
                chess_coord[1].append((x, y))
            else:
                chessboard[(x, y)] = 0
    for i, j in zip([0] * 11, range(11)):
        chessboard[(i, j)] = 1
        chessboard[(11 - i, 11 - j)] = 1
        chessboard[(j, 11)] = 1
        chessboard[(11 - j, 0)] = 1
    si=Simulator(chessboard,False,chess_coord,2000)
    si.simulate()
    # print(si.win_num)
