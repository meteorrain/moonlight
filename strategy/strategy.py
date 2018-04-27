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


# child_num = 2300
# node_num = 200000
# UCB_COEF = 1
# simulate_num = 1
# min_visit_num = 30
# max_visit_num = 1000000
# process_num = 3
# virtual_loss = 2.0


# 策略基本实现
class Strategy:
    def __init__(self, chessboard, status, chess_coord, blank, node_num, UCB_COEF, simulate_num, min_visit_num,
                 max_visit_num, process_num, virtual_loss):
        self.chessboard = chessboard
        self.blank = blank
        self.broadChange()
        self.status = status
        self.chess_coord = chess_coord
        self.UCB_COEF = UCB_COEF
        self.simulate_num = simulate_num
        self.min_visit_num = min_visit_num
        self.max_visit_num = max_visit_num
        self.process_num = process_num
        self.virtual_loss = virtual_loss
        self.convert()
        self.state_space = RawArray(Node, node_num)
        self.curr_num = RawValue(c_int, 0)
        self.max_depth = RawValue(c_int, 0)
        self.test = RawValue(c_int, 0)
        self.time = RawValue(c_double, 0.0)

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
    def search_init(self):
        self.state_space[self.curr_num.value] = Node(self.curr_num, self.status, 0, 0, 0.0, self.blank, False,
                                                     self.c_chessboard,
                                                     self.c_chess_coord, -1,
                                                     children_num=0)
        self.curr_num.value += 1
        # test = time()
        expand_first(self.state_space, self.curr_num, 0)
        print(self.state_space[0].children_num)
        # print(self.curr_num.value)
        # print("expand()%f" % (time() - test))
        self.process = []
        lock = Lock()
        for i in range(self.process_num):
            self.process.append(
                Process(target=strategy_conduct, args=(
                lock, self.max_depth, self.state_space, self.curr_num, self.min_visit_num, self.max_visit_num,
                self.virtual_loss, self.process_num, self.simulate_num, self.UCB_COEF)))
            # Process(target=strategy_conduct,
            #         args=(lock, self.max_depth, self.state_space, self.curr_num, self.test, self.time)))

    def search_start(self):
        for i in range(self.process_num):
            self.process[i].start()

    def search_stop(self):
        for i in range(self.process_num):
            self.process[i].terminate()
        self.record_num=self.state_space[0].visit_num
        print(self.state_space[0].visit_num)
        print(self.max_depth.value)
        print(self.curr_num.value)
        # print(self.state_space[0].children_num)
        # try:
        #     for i in range(self.state_space[0].children_num):
        #         print(self.state_space[self.state_space[0].children[i]].visit_num)
        #         print(self.state_space[self.state_space[0].children[i]].value)
        # except Exception as e:
        #     print(e)

    def get_result(self):
        print(self.state_space[0].visit_num)
        print(self.max_depth.value)
        print(self.curr_num.value)
        # print(self.test.value)
        # print(self.time.value / self.test.value)
        site = select_best_node(self.state_space)
        print(site)
        print("haha")
        self.result = self.state_space[site].move
        for i in range(6):
            print(self.result[i])

    def get_all_children(self):
        self.children = []
        for i in range(self.state_space[0].children_num):
            temp = []
            site = self.state_space[0].children[i]
            for j in range(6):
                temp.append(self.state_space[site].move[j])
            temp.append(self.state_space[site].win_num)
            temp.append(self.state_space[site].visit_num)
            self.children.append(temp)


# 选择收益最佳的子结点
def select_best_node(state_space):
    result = 0
    maxvalue = -10
    for i in range(state_space[0].children_num):
        site = state_space[0].children[i]
        print(state_space[site].value)
        if state_space[site].value > maxvalue:
            maxvalue = state_space[site].value
            result = site
    return result


# 执行策略
def strategy_conduct(lock, depth, state_space, curr_num, min_visit_num, max_visit_num, virtual_loss, process_num,
                     simulate_num, UCB_COEF):
    # def strategy_conduct(lock, depth, state_space, curr_num, test, timet):
    while True:
        # test.value += 1
        if state_space[0].visit_num > max_visit_num:
            return
        site = 0
        curr_depth = 1

        # test1 = time()
        # 选择节点
        while state_space[site].isExpand == True:
            site = select_node(state_space, site, min_visit_num, UCB_COEF)
            state_space[site].value -= virtual_loss
            curr_depth += 1
        # test2 = time()
        # print("选择%f" % (test2 - test1))
        # 扩展节点
        if state_space[site].visit_num >= min_visit_num + process_num + 2:
            with lock:
                flag = expand(state_space, curr_num, site)
            if flag == None:
                site = select_node(state_space, site, min_visit_num, UCB_COEF)
                state_space[site].value -= virtual_loss
                curr_depth += 1
        if curr_depth > depth.value:
            # with lock:
            depth.value = curr_depth
        # test3 = time()
        # print("扩展%f" % (test3 - test2))

        # 模拟游戏
        simulate = Simulator(state_space[site].chessboard, state_space[site].status, state_space[site].chess_coord,
                             simulate_num)
        simulate.simulate()

        # test4 = time()

        # 回溯更新
        # if simulate.win_num == 1:
        #     while site != -1:
        #         with lock:
        #             state_space[site].visit_num += 1
        #             state_space[site].win_num += 1
        #             state_space[site].value = state_space[site].win_num / state_space[site].visit_num
        #         site = state_space[site].parent
        # else:
        #     while site != -1:
        #         with lock:
        #             state_space[site].visit_num += 1
        #             state_space[site].value = state_space[site].win_num / state_space[site].visit_num
        #         site = state_space[site].parent
        if simulate.win_num == 1:
            with lock:
                while site != -1:
                    state_space[site].visit_num += 1
                    state_space[site].win_num += 1
                    state_space[site].value = state_space[site].win_num / state_space[site].visit_num
                    site = state_space[site].parent
        else:
            with lock:
                while site != -1:
                    state_space[site].visit_num += 1
                    state_space[site].value = state_space[site].win_num / state_space[site].visit_num
                    site = state_space[site].parent
        # x = time() - test4
        # print("更新%f" % (x))
        # timet.value += x
        # print("更新%f" % (time() - test4))


# 首次完全扩展
def expand_first(state_space, curr_num, location):
    state_space[location].isExpand = True
    movegenerator = MoveGenerator_first(state_space, location, curr_num)
    movegenerator.collectAllMove()


# 递归选择UCB值最大的叶结点
def select_node(state_space, location, min_visit_num, UCB_COEF):
    curr_node = state_space[location]
    max_ucb = -100000
    result = 0
    for i in range(curr_node.children_num):
        site = curr_node.children[i]
        if state_space[site].visit_num < min_visit_num:
            return site
        ucb = state_space[site].value + UCB_COEF * sqrt(log(curr_node.visit_num) / state_space[site].visit_num)
        if state_space[site].status == state_space[0].status:
            ucb = -ucb
        if ucb > max_ucb:
            max_ucb = ucb
            result = site
    return result


# 扩展结点（随机剪枝）
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
