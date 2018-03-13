# -*- coding: utf-8 -*-
# @create_time: 2018/3/13
# @athor: RuiQing Chen
# @definition:

from copy import deepcopy
from movegenerator import MoveGenerator
from evaluator import Evaluator


class Node:
    def __init__(self, chessboard, status, chess_coord, parent=None):
        self.status = 0 if status == 3 else 1
        self.chessboard = deepcopy(chessboard)
        self.chess_coord = chess_coord[:]
        self.parent = parent
        self.children = []
        self.visit_num = 0
        self.win_num = 0
        self.value = 0
        self.isExpand = False

    def expand(self):
        if self.isExpand:
            return False
        else:
            movegenerator = MoveGenerator(self.chessboard, self.status, self.chess_coord)
            movegenerator.collectAllMove()
            min = 10000
            max = -10000
            for move in movegenerator.allMove:

                self.executeMove(move)

                move.value = Evaluator(self.chessboard, 1 - self.status, self.chess_coord)
                if move.value > max:
                    max = move.value
                if move.value < min:
                    min = move.value

                self.cancelMove(move)

            # 剪枝公式
            threshold = min + (max - min) * 0.618
            for move in movegenerator.allMove:
                if move.value >= threshold:
                    self.executeMove(move)
                    self.children.append(Node(self.chessboard, 1 - self.status, self.chess_coord))
                    self.cancelMove(move)

            self.isExpand = True

    def executeMove(self, move):
        self.chessboard[(move.x, move.y)] = self.chessboard[(move.last_x, move.last_y)]
        self.chessboard[(move.last_x, move.last_y)] = 0
        self.chessboard[(move.arr_x, move.arr_y)] = 1
        self.chess_coord[self.status].remove((move.last_x, move.last_y))
        self.chess_coord[self.status].append((move.x, move.y))

    def cancelMove(self, move):
        self.chess_coord[self.status].remove((move.x, move.y))
        self.chess_coord[self.status].append((move.last_x, move.last_y))
        self.chessboard[(move.last_x, move.last_y)] = self.chessboard[(move.x, move.y)]
        self.chessboard[(move.x, move.y)] = 0
        self.chessboard[(move.arr_x, move.arr_y)] = 0

    def clone(self):
        clone_node = Node(self.chessboard, self.status, self.chess_coord)
        clone_node.children.append(self.children)
        clone_node.visit_num = self.visit_num
        clone_node.win_num = self.win_num
        clone_node.value = self.value
        clone_node.isExpand = self.isExpand
