# -*- coding: utf-8 -*-
'''
@time： 2018/3/7
@author: RuiQing Chen
@definition:gameForwardStack:
            gameBackwardStack:
            currentMove:
            chessBroadRecord:
            currentChessBroadFlag:
            currentChessBroad:
'''
from copy import deepcopy


class gameRecorder():
    def __init__(self):
        self.gameForwardStack = []
        self.gameBackwardStack = []
        self.currentMove = []
        self.chessBroadRecord = []
        self.currentChessBroadFlag = -1
        self.currentChessBroad = {}

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
    def storeChessBroad(self):
        self.chessBroadRecord.append(deepcopy(self.currentChessBroad))
        self.currentChessBroadFlag += 1
        self.currentChessBroad.clear()

    # 获得上一步的棋局
    def getLastChessBroad(self):
        lastChessBroad = {}
        flag = self.currentChessBroadFlag
        if flag >= 1:
            lastChessBroad = self.currentChessBroad[flag]
            self.currentChessBroadFlag -= 1
        return lastChessBroad

    # 获得下一步的棋局
    def getNextChessBroad(self):
        nextChessBroad = {}
        flag = self.currentChessBroadFlag
        if flag < len(self.currentChessBroad) - 1:
            nextChessBroad = self.currentChessBroad[flag]
            self.currentChessBroadFlag += 1
        return nextChessBroad

    # 获得五步之前的棋局
    def getLastFifthChessBroad(self):
        lastFifthChessBroad = {}
        flag = self.currentChessBroadFlag
        if flag >= 5:
            lastFifthChessBroad = self.currentChessBroad[flag]
            self.currentChessBroadFlag -= 5
        return lastFifthChessBroad

    # 获得五步之后的棋局
    def getNextFifthChessBroad(self):
        nextFifthChessBroad = {}
        flag = self.currentChessBroadFlag
        if flag < len(self.currentChessBroad) - 5:
            nextFifthChessBroad = self.currentChessBroad[flag]
            self.currentChessBroadFlag += 5
        return nextFifthChessBroad

    # 获得初始局面
    def getBeginChessBroad(self):
        beginChessBroad = {}
        if len(self.currentChessBroad):
            beginChessBroad = self.currentChessBroad[0]
            self.currentChessBroadFlag = 0
        return beginChessBroad

    # 获得最终局面
    def getEndChessBroad(self):
        endChessBroad = {}
        index = len(self.currentChessBroad)
        if index:
            endChessBroad = self.currentChessBroad[index - 1]
            self.currentChessBroadFlag = index - 1
        return endChessBroad

    # 清除容器内容
    def clear(self):
        self.chessBroadRecord.clear()
        self.gameForwardStack.clear()
        self.gameBackwardStack.clear()
        self.currentMove.clear()
        self.currentChessBroad.clear()
        self.currentChessBroadFlag = -1
