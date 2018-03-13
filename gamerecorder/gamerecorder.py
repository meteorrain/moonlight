# -*- coding: utf-8 -*-
# @time： 2018/3/7
# @author: RuiQing Chen
# @definition:gameForwardStack:
#             gameBackwardStack:
#             currentMove:
#             chessBoardRecord:
#             currentChessBoardFlag:
#             currentChessBoard:

from copy import deepcopy


class GameRecorder:
    def __init__(self):
        self.gameForwardStack = []
        self.gameBackwardStack = []
        self.currentMove = []
        self.chessBoardRecord = []
        self.currentChessBoardFlag = -1
        self.currentChessBoard = {}

    # 存储走法
    def storeMove(self):
        self.gameForwardStack.append(tuple(self.currentMove))
        self.currentMove.clear()

    # 获得上一步走法
    def getLastStep(self):
        lastStep = []
        if len(self.gameForwardStack):
            lastStep.append(self.gameForwardStack.pop())
            self.gameBackwardStack.append(lastStep)
        return lastStep

    # 获得下一步走法
    def getNextStep(self):
        nextStep = []
        if len(self.gameBackwardStack):
            nextStep.append(self.gameBackwardStack.pop())
            self.gameForwardStack.append(nextStep)
        return nextStep

    # 获得上五步走法
    def getLastFiveStep(self):
        lastFiveStep = []
        for i in range(5):
            if len(self.gameForwardStack) > 0:
                lastFiveStep.append(self.gameForwardStack.pop())
            else:
                break
        return lastFiveStep

    # 获得下五步走法
    def getNextFiveStep(self):
        nextFiveStep = []
        for i in range(5):
            if len(self.gameBackwardStack) > 0:
                nextFiveStep.append(self.gameBackwardStack.pop())
            else:
                break
        return nextFiveStep

    # 获得从现局到开局的所有走法
    def getLastAllStep(self):
        lastAllStep = []
        while len(self.gameForwardStack):
            lastAllStep.append(self.gameForwardStack.pop())
        return lastAllStep

    # 获得从现局到终局的所有走法
    def getNextAllStep(self):
        nextAllStep = []
        while len(self.gameBackwardStack):
            nextAllStep.append(self.gameBackwardStack.pop())
        return nextAllStep

    # 存储棋局
    def storeChessBoard(self):
        self.chessBoardRecord.append(deepcopy(self.currentChessBoard))
        self.currentChessBoardFlag += 1
        self.currentChessBoard.clear()

    # 获得上一步的棋局
    def getLastChessBoard(self):
        lastChessBoard = {}
        flag = self.currentChessBoardFlag
        if flag >= 1:
            lastChessBoard = self.currentChessBoard[flag]
            self.currentChessBoardFlag -= 1
        return lastChessBoard

    # 获得下一步的棋局
    def getNextChessBoard(self):
        nextChessBoard = {}
        flag = self.currentChessBoardFlag
        if flag < len(self.currentChessBoard) - 1:
            nextChessBoard = self.currentChessBoard[flag]
            self.currentChessBoardFlag += 1
        return nextChessBoard

    # 获得五步之前的棋局
    def getLastFifthChessBoard(self):
        lastFifthChessBoard = {}
        flag = self.currentChessBoardFlag
        if flag >= 5:
            lastFifthChessBoard = self.currentChessBoard[flag]
            self.currentChessBoardFlag -= 5
        return lastFifthChessBoard

    # 获得五步之后的棋局
    def getNextFifthChessBoard(self):
        nextFifthChessBoard = {}
        flag = self.currentChessBoardFlag
        if flag < len(self.currentChessBoard) - 5:
            nextFifthChessBoard = self.currentChessBoard[flag]
            self.currentChessBoardFlag += 5
        return nextFifthChessBoard

    # 获得初始局面
    def getBeginChessBoard(self):
        beginChessBoard = {}
        if len(self.currentChessBoard):
            beginChessBoard = self.currentChessBoard[0]
            self.currentChessBoardFlag = 0
        return beginChessBoard

    # 获得最终局面
    def getEndChessBoard(self):
        endChessBoard = {}
        index = len(self.currentChessBoard)
        if index:
            endChessBoard = self.currentChessBoard[index - 1]
            self.currentChessBoardFlag = index - 1
        return endChessBoard

    # 清除容器内容
    def clear(self):
        self.chessBoardRecord.clear()
        self.gameForwardStack.clear()
        self.gameBackwardStack.clear()
        self.currentMove.clear()
        self.currentChessBoard.clear()
        self.currentChessBoardFlag = -1
