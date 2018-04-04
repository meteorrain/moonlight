# -*- coding: utf-8 -*-
# create_time：2018/3/9
# reconstruct: 2018/3/26    original method can not fit multiprocess, so I do some change.
# author: RuiQing Chen
# definition:


from ctypes import Structure, c_double, c_int, c_bool
from multiprocessing.sharedctypes import RawValue, RawArray
from multiprocessing import Lock, Process
from math import sqrt, log
from movegenerator import MoveGenerator, Node
from movegenerator_first import MoveGenerator_first
from simulator import Simulator
# from simulator1 import Simulator
from threading import Thread
from time import time, sleep

child_num = 2300
node_num = 200000
UCB_COEF = 1
simulate_num = 1
min_visit_num = 50
max_visit_num = 1000000
time_limit = 10
process_num = 6
virtual_loss = 2.0


# 等待所有进程结束
class Count_time(Thread):
    def __init__(self, process, num):
        super(Count_time, self).__init__()
        self.process = process
        self.num = num

    def run(self):
        while True:
            flag = 0
            for i in range(self.num):
                if self.process[i].is_alive() == True:
                    flag = 1
                    break
            if flag == 0:
                break
            sleep(0.1)


# 策略基本实现
class Strategy:
    def __init__(self, chessboard, status, chess_coord, blank):
        self.chessboard = chessboard
        self.blank = blank
        self.broadChange()
        self.status = False if status == 3 else True
        self.chess_coord = chess_coord
        self.convert()
        self.state_space = RawArray(Node, node_num)
        self.curr_num = RawValue(c_int, 0)
        self.max_depth = RawValue(c_int, 0)
        self.test = RawValue(c_int, 0)
        self.time=RawValue(c_double,0.0)
        self.result = self.getResult()

    # 棋盘外加保护边界用于估值以及走法生成
    def broadChange(self):
        for i, j in zip([0] * 11, range(11)):
            self.chessboard[(i, j)] = 1
            self.chessboard[(11 - i, 11 - j)] = 1
            self.chessboard[(j, 11)] = 1
            self.chessboard[(11 - j, 0)] = 1

    # 将前端UI传入的字典和元组转换为Structure可以初始化的对象
    def convert(self):
        # 转换棋盘
        collect = []
        for i in range(12):
            temp = []
            for j in range(12):
                temp.append(self.chessboard[(i, j)])
            collect.append(tuple(temp))
        self.c_chessboard = tuple(collect)

        # 转化棋子坐标
        collect.clear()
        for i in range(2):
            temp.clear()
            for j in range(4):
                temp.append(self.chess_coord[i][j][0])
                temp.append(self.chess_coord[i][j][1])
            collect.append(tuple(temp))
        self.c_chess_coord = tuple(collect)

    # 获得最终结果
    def getResult(self):
        self.state_space[self.curr_num.value] = Node(self.curr_num, self.status, 0, 0, 0.0, self.blank, False,
                                                     self.c_chessboard,
                                                     self.c_chess_coord, -1,
                                                     children_num=0)
        self.curr_num.value += 1
        test = time()
        expand_first(self.state_space, self.curr_num, 0)
        print(self.curr_num.value)
        print("expand()%f" % (time() - test))
        process = []
        lock = Lock()
        for i in range(process_num):
            process.append(
                # Process(target=strategy_conduct, args=(lock, self.max_depth, self.state_space, self.curr_num)))
                Process(target=strategy_conduct,
                        args=(lock, self.max_depth, self.state_space, self.curr_num, self.test,self.time)))
        for i in range(process_num):
            process[i].start()
        counter = Count_time(process, process_num)
        counter.start()
        counter.join(time_limit)
        for i in range(process_num):
            process[i].terminate()
        print(self.state_space[0].visit_num)
        print(self.max_depth.value)
        print(self.test.value)
        print(self.time.value/self.test.value)
        site = select_best_node(self.state_space)
        return self.state_space[site].move

# 选择收益最佳的子结点
def select_best_node(state_space):
    result = 0
    maxvalue = -1
    for i in range(state_space[0].children_num):
        site = state_space[0].children[i]
        if state_space[site].value > maxvalue:
            maxvalue = state_space[site].value
            result = site
    return result


# 执行策略
# def strategy_conduct(lock, depth, state_space, curr_num):
def strategy_conduct(lock, depth, state_space, curr_num, test,timet):
    while True:
        test.value += 1
        if state_space[0].visit_num > max_visit_num:
            return
        site = 0
        curr_depth = 1

        test1 = time()
        # 选择节点
        while state_space[site].isExpand == True:
            site = select_node(state_space, site)
            state_space[site].value -= virtual_loss
            curr_depth += 1
        test2 = time()
        print("选择%f" % (test2 - test1))
        # 扩展节点
        if state_space[site].visit_num >= min_visit_num:
            with lock:
                flag = expand(state_space, curr_num, site)
            if flag == None:
                site = select_node(state_space, site)
                state_space[site].value -= virtual_loss
                curr_depth += 1
        if curr_depth > depth.value:
            with lock:
                depth.value = curr_depth
        test3 = time()
        print("扩展%f" % (test3 - test2))

        # 模拟游戏
        simulate = Simulator(state_space[site].chessboard, state_space[site].status, state_space[site].chess_coord,
                             simulate_num)
        simulate.simulate()

        test4 = time()
        x=test4 - test3
        print("模拟%f" % (x))
        timet.value+=x
        # 回溯更新
        if simulate.win_num == 1:
            while site != -1:
                with lock:
                    state_space[site].visit_num += 1
                    state_space[site].win_num += 1
                    state_space[site].value = state_space[site].win_num / state_space[site].visit_num
                site = state_space[site].parent
        else:
            while site != -1:
                with lock:
                    state_space[site].visit_num += 1
                    state_space[site].value = state_space[site].win_num / state_space[site].visit_num
                site = state_space[site].parent
        print("更新%f" % (time() - test4))

# 扩展结点
def expand(state_space, curr_num, location):
    node = state_space[location]
    if node.isExpand:
        return False
    else:
        movegenerator = MoveGenerator(state_space, location, curr_num)
        movegenerator.collectAllMove()
        if node.children_num == 0:
            return True
        node.isExpand = True

# 首次完全扩展
def expand_first(state_space, curr_num, location):
    state_space[location].isExpand = True
    movegenerator = MoveGenerator_first(state_space, location, curr_num)
    movegenerator.collectAllMove()

# 递归选择UCB值最大的叶结点
def select_node(state_space, location):
    curr_node = state_space[location]
    max_ucb = -100000
    result = 0
    for i in range(curr_node.children_num):
        site = curr_node.children[i]
        if state_space[site].visit_num < min_visit_num:
            return site
        ucb = state_space[site].value + sqrt(log(curr_node.visit_num) / state_space[site].visit_num)
        if state_space[site].status == state_space[0].status:
            ucb = -ucb
        if ucb > max_ucb:
            max_ucb = ucb
            result = site
    return result
