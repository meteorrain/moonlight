# -*- coding: utf-8 -*-

# @time： 2018/2/25
# @author: RuiQing Chen
# @definition:mode: 1——人人  2——人机  3——机机
#             status: 1——人（正方）  2——人（反方）  3——机（正方）  4——机（反方）  5——暂停  6——停止
#             clicktimes:控制棋局中鼠标点击次数
#             times:控制工具栏的显示

import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gamerule import GameRule
from gamerecorder import GameRecorder
from copy import deepcopy


# 用于显示电脑招数的线程
class WorkThread(QThread):
    returnResult = pyqtSignal(list)  # 自定义主线程与子线程间通信信号

    def __init__(self, interFace):
        self.interFace = interFace
        super(WorkThread, self).__init__()

    # 重写线程运行函数
    def run(self):
        while True:
            self.sleep(0.5)  # 子线程每隔0.5秒查询一次
            if (self.interFace.mode == 2 or self.interFace.mode == 3) \
                    and (
                    self.interFace.status == 3 or self.interFace.status == 4) and self.interFace.antiThreadFlag == 0:
                pass
                if self.interFace.status == 3:
                    self.interFace.currentChess = 2
                else:
                    self.interFace.currentChess = 3
                self.interFace.antiThreadFlag = 1
                self.result = self.interFace.computeData()
                self.returnResult.emit(self.result)


# 主窗口
class InterFace(QMainWindow):
    # 初始化主界面
    def __init__(self, parent=None):
        super(InterFace, self).__init__(parent)
        self.resize(1100, 800)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(1100, 800)
        self.setWindowTitle("moonlight")
        settings = QSettings("configure", QSettings.NativeFormat)
        self.status = settings.value("status", 1)
        self.mode = settings.value("mode", 1)
        self.gamerecord = GameRecorder()
        self.game = GameRule()
        self.initBoard()
        self.menuLayout()
        self.toolLayout()
        self.displayBoard()
        self.center()
        if self.mode == 2 or self.mode == 3:
            self.workthread = WorkThread(self)
            self.workthread.returnResult.connect(self.threadConduct)
            self.antiThreadFlag = 0  # 开启子线程响应
            self.workthread.start()

    '''
    以下为子线程获取电脑走法的界面显示函数
    '''

    # 线程处理槽函数
    def threadConduct(self, result):
        self.chessboard[(result[0], result[1])] = 0
        self.chessboard[(result[2], result[3])] = self.currentChess
        if self.currentChess == 2:
            self.chess_coord[0].remove((result[0], result[1]))
            self.chess_coord[0].append((result[2], result[3]))
        else:
            self.chess_coord[1].remove((result[0], result[1]))
            self.chess_coord[1].append((result[2], result[3]))
        self.sequentAnimation = QSequentialAnimationGroup()
        self.threadChessMove(result[0], result[1], result[2], result[3])
        self.chessboard[(result[4], result[5])] = 1
        self.blank -= 1
        self.threadShootArrow(result[2], result[3], result[4], result[5])
        self.antimouse = 1
        self.sequentAnimation.start()
        self.clicktimes += 3
        self.judgeIsover()

    # 界面上显示电脑实时搜索情况
    def realTimeDataConduct(self, estimation, sum):
        while True:
            time.sleep(1)
            if self.status == 3 or self.status == 4:
                self.display.setText(self.text)
            else:
                break

    # 线程处理时的棋子移动函数
    def threadChessMove(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        list = self.chess.childAt(QPoint(lx * offset + 2, (11 - ly) * offset + 2))
        if self.currentChess == 2:
            list.setPixmap(QPixmap("./images/chess_white.png"))
        else:
            list.setPixmap(QPixmap("./images/chess_black.png"))
        list.setProperty("coordx", x)
        list.setProperty("coordy", y)
        self.animation = QPropertyAnimation(list, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2))
        self.sequentAnimation.addAnimation(self.animation)

    # 线程处理时的动图播放函数
    def threadPlayMovie(self):
        self.movie = QMovie("./images/balltosquare.gif")
        self.ba.setMovie(self.movie)
        self.movie.start()

    # 设置图片，用于动画结束的槽函数
    def setPix(self):
        self.ba.setPixmap(QPixmap("./images/ball.png"))

    # 线程处理时发射障碍函数
    def threadShootArrow(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        ba = self.labelList.pop()
        self.ba = ba
        self.animation1 = QPropertyAnimation(ba, b"pixmap")
        self.animation1.setDuration(100)
        self.animation1.finished.connect(self.setPix)
        self.sequentAnimation.addAnimation(self.animation1)
        ba.setScaledContents(True)
        ba.setGeometry(lx * offset + 2, (11 - ly) * offset + 2, offset - 2, offset - 2)
        ba.setProperty("coordx", x)
        ba.setProperty("coordy", y)
        self.animation = QPropertyAnimation(ba, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 1.5, (11 - y) * offset + 1.5, offset - 2, offset - 2))
        self.sequentAnimation.addAnimation(self.animation)
        self.animation.finished.connect(self.threadPlayMovie)

    # 电脑搜索走法函数
    def computeData(self):
        pass

    '''
    以下为主线程UI逻辑函数
    '''

    # 设置菜单栏
    def menuLayout(self):
        self.bar = self.menuBar()
        # 游戏的子菜单
        game = self.bar.addMenu(" 游  戏 ")
        newgame = QAction("新游戏", self)
        newgame.setShortcut("F5")
        game.addAction(newgame)
        pausegame = QAction("暂停游戏", self)
        pausegame.setShortcut("F6")
        game.addAction(pausegame)
        stopgame = QAction("停止游戏", self)
        stopgame.setShortcut("F7")
        game.addAction(stopgame)
        game.addSeparator()
        open = QAction("打开", self)
        open.setShortcut("Ctrl+O")
        game.addAction(open)
        save = QAction("保存", self)
        save.setShortcut("Ctrl+S")
        game.addAction(save)
        game.addSeparator()
        quit = QAction("退出", self)
        quit.setShortcut("Ctrl+Q")
        game.addAction(quit)
        # 棋局控制的子菜单
        situation = self.bar.addMenu("棋局控制")
        up = QAction("后退一步", self)
        up.setShortcut("F9")
        situation.addAction(up)
        down = QAction("前进一步", self)
        down.setShortcut("F10")
        situation.addAction(down)
        up5 = QAction("后退五步", self)
        up5.setShortcut("F11")
        situation.addAction(up5)
        down5 = QAction("前进五步", self)
        down5.setShortcut("F12")
        situation.addAction(down5)
        start = QAction("回到开局", self)
        start.setShortcut("F1")
        situation.addAction(start)
        end = QAction("直达终局", self)
        end.setShortcut("F2")
        situation.addAction(end)
        # 移动控制的子菜单
        movecontrol = self.bar.addMenu("移动控制")
        movenow = QAction("强制落子", self)
        movenow.setShortcut("Ctrl+R")
        movecontrol.addAction(movenow)
        suggest = QAction("走法建议", self)
        movecontrol.addAction(suggest)
        coordmove = QAction("坐标落子", self)
        movecontrol.addAction(coordmove)
        switchside = QAction("转换角色", self)
        movecontrol.addAction(switchside)
        # 设置的子菜单
        setting = self.bar.addMenu(" 设  置 ")
        appearance = QAction("界面设置", self)
        setting.addAction(appearance)
        setting.addSeparator()
        gamemode = QAction("对战模式", self)
        setting.addAction(gamemode)
        parallelmode = QAction("并行模式", self)
        setting.addAction(parallelmode)
        setting.addSeparator()
        parameter = QAction("算法参数", self)
        parameter.setShortcut("Ctrl+H")
        setting.addAction(parameter)
        # 视图的子菜单
        view = self.bar.addMenu(" 视  图 ")
        self.toolcolumn = QAction("工具栏", self)
        self.toolcolumn.setShortcut("Ctrl+T")
        # self.toolcolumn.setObjectName("toolcolumn")
        self.toolcolumn.setIcon(QIcon("./images/checked.png"))
        self.toolcolumn.triggered.connect(self.displayToolbar)
        view.addAction(self.toolcolumn)
        textbox = QAction("文本框", self)
        view.addAction(textbox)
        movehistory = QAction("博弈实况", self)
        view.addAction(movehistory)
        # 关于的子菜单
        about = self.bar.addMenu(" 帮  助 ")
        copyinfo = QAction("关于moonlight", self)
        copyinfo.setShortcut("Ctrl+I")
        about.addAction(copyinfo)
        help = QAction("技术相关", self)
        about.addAction(help)

    # 设置工具栏
    def toolLayout(self):
        self.tb = QToolBar()
        self.tb.setObjectName("tb")
        start = QAction(QIcon("./images/Start.png"), "开始&继续", self)
        self.tb.addAction(start)
        pause = QAction(QIcon("./images/Pause.png"), "暂停", self)
        self.tb.addAction(pause)
        stop = QAction(QIcon("./images/Stop_red.png"), "停止", self)
        self.tb.addAction(stop)
        self.tb.addSeparator()
        open = QAction(QIcon("./images/open_file.png"), "打开", self)
        self.tb.addAction(open)
        save = QAction(QIcon("./images/Save.png"), "保存", self)
        self.tb.addAction(save)
        self.tb.addSeparator()
        Hide_left_left = QAction(QIcon("./images/Hide_left_left.png"), "回到开局", self)
        self.tb.addAction(Hide_left_left)
        Hide_left = QAction(QIcon("./images/Hide_left.png"), "后退五步", self)
        self.tb.addAction(Hide_left)
        left = QAction(QIcon("./images/left.png"), "后退一步", self)
        self.tb.addAction(left)
        right = QAction(QIcon("./images/right.png"), "前进一步", self)
        self.tb.addAction(right)
        Hide_right = QAction(QIcon("./images/Hide_right.png"), "前进五步", self)
        self.tb.addAction(Hide_right)
        Hide_right_right = QAction(QIcon("./images/Hide_right_right.png"), "直达终局", self)
        self.tb.addAction(Hide_right_right)
        self.tb.addSeparator()
        Prohibit = QAction(QIcon("./images/Prohibit.png"), "强制落子", self)
        self.tb.addAction(Prohibit)
        Refresh = QAction(QIcon("./images/refresh.png"), "刷新棋盘", self)
        self.tb.addAction(Refresh)
        Analyze = QAction(QIcon("./images/Analyze.png"), "分析", self)
        self.tb.addAction(Analyze)
        Suggest = QAction(QIcon("./images/Suggest.png"), "建议", self)
        self.tb.addAction(Suggest)
        self.tb.addSeparator()
        Situation = QAction(QIcon("./images/Situation.png"), "博弈实况", self)
        self.tb.addAction(Situation)
        Info = QAction(QIcon("./images/Info.png"), "文本窗口", self)
        self.tb.addAction(Info)
        Setting = QAction(QIcon("./images/Setting.png"), "设置", self)
        self.tb.addAction(Setting)
        self.tb.addSeparator()
        Sound = QAction(QIcon("./images/Sound.png"), "声音", self)
        self.tb.addAction(Sound)
        self.addToolBar(self.tb)

    # 将窗口移至屏幕中心
    def center(self):
        # 获取屏幕坐标数据
        screen = QDesktopWidget().screenGeometry()
        # 获取调用对象的坐标数据
        size = self.geometry()
        # 移动作用于调用对象的中心位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # 显示工具栏
    def displayToolbar(self):
        if self.times == 0:
            self.times = 1
            self.toolcolumn.setIcon(QIcon("./images/checked.png"))
            self.tb.setVisible(True)
        else:
            self.times = 0
            self.toolcolumn.setIcon(QIcon())
            self.tb.setVisible(False)

    # 初始化棋盘
    def initBoard(self):
        self.chessboard = {}
        self.times = 1
        self.clicktimes = 0
        self.lastx = -1
        self.lasty = -1
        self.blank = 92
        self.labelList = []
        self.chess_coord = []
        self.chess_coord.append([])
        self.chess_coord.append([])
        self.antimouse = 0
        # 此处需要加上显示棋子的label的清除
        for x in range(1, 11):
            for y in range(1, 11):
                if x == 1 and y == 4 or x == 4 and y == 1 or x == 7 and y == 1 or x == 10 and y == 4:
                    self.chessboard[(x, y)] = 2
                    self.chess_coord[0].append((x, y))
                elif x == 1 and y == 7 or x == 4 and y == 10 or x == 7 and y == 10 or x == 10 and y == 7:
                    self.chessboard[(x, y)] = 3
                    self.chess_coord[1].append((x, y))
                else:
                    self.chessboard[(x, y)] = 0
        self.gamerecord.clear()
        self.gamerecord.currentChessBroad = deepcopy(self.chessboard)
        self.gamerecord.storeChessBoard()

    # 显示棋盘
    def displayBoard(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.chess = QLabel(self.centralwidget)
        minsize = min(self.centralwidget.width() / 3 * 2 - 40, self.centralwidget.height() - 20)
        self.chess.setGeometry(20, 20, minsize, minsize)
        self.chess.setPixmap(QPixmap("./images/chessboard.png"))
        self.chess.setScaledContents(True)
        self.display = QLabel(self.centralwidget)
        self.display.setFont(QFont("微软雅黑", 12))
        self.display.setAlignment(Qt.AlignTop)
        self.text = "玩家————————————————————————————————————————————————————————\
\n\n    白方：    \n    黑方：    \n\n\n游戏时间————————————————————————————————————————————\
——————————\n\n    白方：    \n    黑方：    \n\n\n当前行为——————————————————————————————————\
————————————————————————\n\n    None\n\n\n状态——————————————————————————————————\
——————————————————————\n\n    游戏状态：    \n    估值：    \n    走法总数：    "
        self.display.setText(self.text)
        self.display.setGeometry(self.centralwidget.width() / 3 * 2, 20, self.centralwidget.width() / 3 - 40,
                                 self.centralwidget.height() - 40)
        # 生成92个待用QLabel作为障碍备用
        for i in range(92):
            self.labelList.append(QLabel(self.chess))

        # 布置棋盘
        offset = self.chess.width() / 12
        for x in range(1, 11):
            for y in range(1, 11):
                if (self.chessboard[(x, y)] == 1):
                    la = QLabel(self.chess)
                    la.setPixmap(QPixmap("./images/obstacle.png"))
                    la.setScaledContents(True)
                    la.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
                    la.setProperty("coordx", x)
                    la.setProperty("coordy", y)
                elif (self.chessboard[(x, y)] == 2):
                    la = QLabel(self.chess)
                    la.setPixmap(QPixmap("./images/chess_white.png"))
                    la.setScaledContents(True)
                    la.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
                    la.setProperty("coordx", x)
                    la.setProperty("coordy", y)
                elif (self.chessboard[(x, y)] == 3):
                    la = QLabel(self.chess)
                    la.setPixmap(QPixmap("./images/chess_black.png"))
                    la.setScaledContents(True)
                    la.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
                    la.setProperty("coordx", x)
                    la.setProperty("coordy", y)

    # 重载窗口大小改变事件
    def resizeEvent(self, event):
        minsize = min(self.centralwidget.width() / 3 * 2 - 40, self.centralwidget.height() - 40)
        self.chess.setGeometry(20, 20, minsize, minsize)
        self.display.setGeometry(self.centralwidget.width() / 3 * 2, 20, self.centralwidget.width() / 3 - 40,
                                 self.centralwidget.height() - 40)
        offset = self.chess.width() / 12
        list = self.chess.children()
        for x in list:
            if x.property("coordx") is not None:
                x.setGeometry(x.property("coordx") * offset + 2, (11 - x.property("coordy")) * offset + 2,
                              offset - 2, offset - 2)

    # 重载鼠标单击事件
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton or event.button() == Qt.RightButton) \
                and (self.status == 1 or self.status == 2) and self.antimouse == 0:
            offset = self.chess.width() / 12
            x = (event.x() - self.centralwidget.x() - 20) // offset
            y = (event.y() - self.centralwidget.y() - 20) // offset
            if x >= 1 and x <= 10 and y >= 1 and y <= 10:
                x = int(x)
                y = int(11 - y)
                self.antithreadFlag = 1  # 使子线程处于等待状态
                # 鼠标左击进入逻辑判断
                if event.button() == Qt.LeftButton:
                    self.clicktimes += 1
                    self.logicJudge(x, y)
                # 鼠标右击进入取消选中操作
                else:
                    if self.chessboard[(x, y)] == 2 or self.chessboard[(x, y)] == 3:
                        list = self.chess.childAt(QPoint(x * offset + 2, (11 - y) * offset + 2))
                        if list.movie() is not None:
                            if self.chessboard[(x, y)] == 2:
                                list.setPixmap(QPixmap("./images/chess_white.png"))
                            else:
                                list.setPixmap(QPixmap("./images/chess_black.png"))
                            self.clicktimes -= 1

    # 发射障碍动画
    def shootArrow(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        ba = self.labelList.pop()
        ba.setPixmap(QPixmap("./images/ball.png"))
        ba.setScaledContents(True)
        ba.setGeometry(lx * offset + 2, (11 - ly) * offset + 2, offset - 2, offset - 2)
        ba.setProperty("coordx", x)
        ba.setProperty("coordy", y)
        self.animation = QPropertyAnimation(ba, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 1.5, (11 - y) * offset + 1.5, offset - 2, offset - 2))
        self.ba = ba
        self.animation.start()
        self.animation.finished.connect(self.freeMouse)
        self.animation.finished.connect(self.playMovie)

    # 属性动画结束后播放movie
    def playMovie(self):
        self.movie = QMovie("./images/balltosquare.gif")
        self.ba.setMovie(self.movie)
        self.movie.start()
        self.movie.finished.connect(self.judgeIsover)

    # 判断棋局是否结束
    def judgeIsover(self):
        self.game.isOver(self.chessboard, self.status, self.chess_coord)
        if self.game.over:
            if self.game.winner == 1:
                QMessageBox.information(self, "游戏结束", "反方获胜！  赢%d" % self.blank + "子", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            elif self.game.winner == 0:
                QMessageBox.information(self, "游戏结束", "正方获胜！  赢%d" % self.blank + "子", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            else:
                QMessageBox.information(self, "游戏结束", "winner不应该为-1,请检查isOver方法！", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
        else:
            if self.mode == 1:
                self.status = 3 - self.status
            elif self.mode == 2:
                if self.status == 1 or self.status == 2:
                    self.status = 5 - self.status
                    self.antiThreadFlag = 0  # 释放子线程响应
                elif self.status == 3 or self.status == 4:
                    self.status = 5 - self.status
                    self.antimouse = 0  # 释放鼠标响应
            elif self.mode == 3:
                self.status = 7 - self.status
                self.antiThreadFlag = 0  # 释放子线程响应

    # 动画播放时禁止鼠标操作
    def freeMouse(self):
        self.antimouse = 0

    # 棋子移动动画
    def chessMove(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        list = self.chess.childAt(QPoint(lx * offset + 2, (11 - ly) * offset + 2))
        if self.currentChess == 2:
            list.setPixmap(QPixmap("./images/chess_white.png"))
        else:
            list.setPixmap(QPixmap("./images/chess_black.png"))
        list.setProperty("coordx", x)
        list.setProperty("coordy", y)
        self.animation = QPropertyAnimation(list, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2))
        self.animation.start()
        self.animation.finished.connect(self.freeMouse)

    # 左键选中棋子
    def selectChess(self, x, y):
        offset = self.chess.width() / 12
        list = self.chess.childAt(QPoint(x * offset + 5, (11 - y) * offset + 5))
        if self.currentChess == 2:
            movie = QMovie("./images/plus.gif")
        else:
            movie = QMovie("./images/minus.gif")
        list.setMovie(movie)
        movie.start()

    # 行为逻辑判断
    def logicJudge(self, x, y):
        c3 = self.clicktimes % 3
        lx = self.lastx
        ly = self.lasty
        if self.chessboard[(x, y)] == 0:
            if c3 == 0:
                if self.game.moveRule(self.chessboard, lx, ly, x, y):
                    self.chessboard[(x, y)] = 1
                    self.blank -= 1
                    self.gamerecord.currentMove.append(x)
                    self.gamerecord.currentMove.append(y)
                    self.gamerecord.currentChessBroad = deepcopy(self.chessboard)
                    self.gamerecord.storeMove()
                    self.gamerecord.storeChessBoard()
                    self.antimouse = 1  # 关闭鼠标响应
                    self.shootArrow(lx, ly, x, y)
                else:
                    self.clicktimes -= 1
                    QMessageBox.information(self, "提示", "不符合发射规则")
                    return 0
            elif c3 == 2:
                if self.game.moveRule(self.chessboard, lx, ly, x, y):
                    self.chessboard[(lx, ly)] = 0
                    self.chessboard[(x, y)] = self.currentChess
                    self.gamerecord.currentMove.append(x)
                    self.gamerecord.currentMove.append(y)
                    if self.currentChess == 2:
                        self.chess_coord[0].remove((lx, ly))
                        self.chess_coord[0].append((x, y))
                    else:
                        self.chess_coord[1].remove((lx, ly))
                        self.chess_coord[1].append((x, y))
                    self.antimouse = 1
                    self.chessMove(lx, ly, x, y)
                else:
                    self.clicktimes -= 1
                    QMessageBox.information(self, "提示", "不符合落子规则")
                    return 0
            else:
                self.clicktimes -= 1
                QMessageBox.information(self, "提示", "此处无棋子")
                return 0
        else:
            if c3 == 0:
                QMessageBox.information(self, "提示", "不符合发射规则")
                self.clicktimes -= 1
                return 0
            elif c3 == 2:
                QMessageBox.information(self, "提示", "不符合落子规则")
                self.clicktimes -= 1
                return 0
            else:
                if self.status == 1 and self.chessboard[(x, y)] == 2:
                    self.currentChess = 2
                    self.gamerecord.currentMove.append(x)
                    self.gamerecord.currentMove.append(y)
                    self.selectChess(x, y)
                    pass
                elif self.status == 2 and self.chessboard[(x, y)] == 3:
                    self.currentChess = 3
                    self.gamerecord.currentMove.append(x)
                    self.gamerecord.currentMove.append(y)
                    self.selectChess(x, y)
                elif self.chessboard[(x, y)] == 1:
                    QMessageBox.information(self, "提示", "此处无棋子")
                    self.clicktimes -= 1
                    return 0
                else:
                    QMessageBox.information(self, "提示", "还没到你下的时候呢")
                    self.clicktimes -= 1
                    return 0
        self.lastx = x
        self.lasty = y
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/moon_128px.ico"))
    form = InterFace()
    form.show()
    sys.exit(app.exec())
