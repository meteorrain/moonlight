# -*- coding: utf-8 -*-
# @time： 2018/2/25
# @author: RuiQing Chen
# @definition:mode: 1——人人  2——人机  3——机机
#             status: 1——人（正方）  2——人（反方）  3——机（正方）  4——机（反方）
#             clicktimes:控制棋局中鼠标点击次数
#             times:控制工具栏的显示

# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
from gamerule import GameRule
from gamerecorder import GameRecorder
from strategy import Strategy
from threading import Thread
from simulator import Simulator
from evaluator import Evaluator
from copy import deepcopy
from time import time, sleep
from socket import socket, AF_INET, SOCK_DGRAM
from json import dumps, loads
from settings import *

time_limit = int(QSettings('configure', QSettings.IniFormat).value('time_limit', 10))


# 等待所有进程结束
class Count_time(Thread):
    def __init__(self, interface, socket, address):
        super(Count_time, self).__init__()
        self.interface = interface
        self.socket = socket
        self.address = address

    def run(self):
        start = time()
        while True:
            curr_time = time()
            if self.interface.stop_flag == True or curr_time - start > time_limit:
                string = 'stop'
                self.socket.sendto(string.encode(encoding='utf-8'), self.address)
                break
            sleep(0.5)


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

            if self.interFace.start_flag == True:
                if (self.interFace.mode == 2 or self.interFace.mode == 3) \
                        and (
                        self.interFace.status == 3 or self.interFace.status == 4) and self.interFace.antiThreadFlag == 0:
                    self.interFace.Prohibit.setEnabled(True)
                    self.interFace.m_move_now.setEnabled(True)
                    self.interFace.set_left_disable()
                    self.interFace.set_right_disable()

                    if self.interFace.status == 3:
                        self.interFace.currentChess = 2
                    else:
                        self.interFace.currentChess = 3
                    self.interFace.antiThreadFlag = 1
                    self.result = self.interFace.computeData()
                    self.sleep(2)
                    self.returnResult.emit(self.result)

                    self.interFace.set_left_enable()
                    self.interFace.set_right_disable()
                    self.interFace.Prohibit.setEnabled(False)
                    self.interFace.m_move_now.setEnabled(False)


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
        self.settings = QSettings("configure", QSettings.IniFormat)

        self.gamerecord = GameRecorder()
        self.game = GameRule()
        self.menuLayout()
        self.toolLayout()
        self.labelList = []
        self.labelList_used = []
        # 生成100个待用QLabel作为障碍备用
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.chess = QLabel(self.centralwidget)
        for i in range(100):
            self.labelList.append(QLabel(self.chess))
        self.openflag = 0
        self.situation = None
        self.white=None
        self.black=None
        self.initBoard()
        self.showLabel()
        self.center()

        self.start_flag = False
        self.stop_flag = False
        self.time_counter = []
        for i in range(2):
            self.time_counter.append(QTime(0, 0, 0, 0))
        self.time_recorder = []
        x1 = QTimer()
        x1.timeout.connect(self.update_time1)
        self.time_recorder.append(x1)
        x2 = QTimer()
        x2.timeout.connect(self.update_time2)
        self.time_recorder.append(x2)
        self.antimouse = 1
        self.run_status = 0
        self.mode_dialog = None
        self.aspect_dialog = None
        self.function_dialog = None
        self.parameter_dialog = None
        self.set_dialog = None
        self.about_dialog = None

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
        if self.currentChess == 2:
            self.action.setText("  正方(机) 从(%d,%d)移至(%d,%d)   " % (result[0], result[1], result[2], result[3]))
            self.show_text += "  正方(机) 从(%d,%d)移至(%d,%d)   \n" % (result[0], result[1], result[2], result[3])
            self.setSituation()
        else:
            self.action.setText("  反方(机) 从(%d,%d)移至(%d,%d)   " % (result[0], result[1], result[2], result[3]))
            self.show_text += "  反方(机) 从(%d,%d)移至(%d,%d)   \n" % (result[0], result[1], result[2], result[3])
            self.setSituation()

        self.threadChessMove(result[0], result[1], result[2], result[3])
        self.chessboard[(result[4], result[5])] = 1
        self.blank -= 1
        for i in range(6):
            self.gamerecord.currentMove.append(result[i])
        self.gamerecord.currentChessBroad = deepcopy(self.chessboard)
        self.gamerecord.storeMove()
        self.gamerecord.storeChessBoard()
        self.gamerecord.clear_history()
        if self.currentChess == 2:
            self.action.setText("  正方(机) 在(%d,%d)处设置障碍   " % (result[4], result[5]))
            self.show_text += "  正方(机) 在(%d,%d)处设置障碍   \n" % (result[4], result[5])
            self.setSituation()
        else:
            self.action.setText("  反方(机) 在(%d,%d)处设置障碍   " % (result[4], result[5]))
            self.show_text += "  反方(机) 在(%d,%d)处设置障碍   \n" % (result[4], result[5])
            self.setSituation()

        self.threadShootArrow(result[2], result[3], result[4], result[5])
        self.antimouse = 1
        self.sequentAnimation.start()
        self.clicktimes += 3
        self.judgeIsover()

    # 线程处理时的棋子移动函数
    def threadChessMove(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        list = self.chess.childAt(QPoint(lx * offset + 2, (11 - ly) * offset + 2))
        if self.currentChess == 2:
            list.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('plus', 'chess_white')))))
        else:
            list.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('minus', 'chess_black')))))
        list.setProperty("coordx", x)
        list.setProperty("coordy", y)
        self.animation = QPropertyAnimation(list, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2))
        self.sequentAnimation.addAnimation(self.animation)

    # 线程处理时的动图播放函数
    def threadPlayMovie(self):
        self.movie = QMovie("./images/%s.gif" % (str(self.settings.value('ball', 'ball'))))
        self.ba.setMovie(self.movie)
        self.movie.start()

    # 设置图片，用于动画结束的槽函数
    def setPix(self):
        self.ba.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('ball', 'ball')))))

    # 线程处理时发射障碍函数
    def threadShootArrow(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        ba = self.labelList.pop()
        self.ba = ba
        self.animation1 = QPropertyAnimation(ba, b"pixmap")
        self.animation1.setDuration(100)
        self.animation1.setEndValue(QPixmap("./images/%s.png" % (str(self.settings.value('ball', 'ball')))))
        self.animation1.finished.connect(self.setPix)
        self.sequentAnimation.addAnimation(self.animation1)
        ba.setVisible(True)
        ba.setScaledContents(True)
        ba.setGeometry(lx * offset + 2, (11 - ly) * offset + 2, offset - 2, offset - 2)
        ba.setProperty("coordx", x)
        ba.setProperty("coordy", y)
        self.labelList_used.append(ba)
        self.animation = QPropertyAnimation(ba, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 1.5, (11 - y) * offset + 1.5, offset - 2, offset - 2))
        self.sequentAnimation.addAnimation(self.animation)
        self.animation.finished.connect(self.threadPlayMovie)

    # 电脑搜索走法函数
    def computeData(self):
        try:
            host = self.settings.value("communicate", "127.0.0.1")
            port = int(self.settings.value("port", 12345))
            compute_port = int(self.settings.value("compute_port", 12306))
            mode = 0
            ip_num = int(self.settings.value("computer_num", 1))
            ip_pack = []
            for i in range(ip_num):
                ip_pack.append(str(self.settings.value("compute%d" % i, '127.0.0.1')))
            # ip_pack = ['127.0.0.1']
            local = socket(AF_INET, SOCK_DGRAM)
            chessboard = []
            for i in range(1, 11):
                temp = []
                for j in range(1, 11):
                    temp.append(self.chessboard[(i, j)])
                chessboard.append(temp)
            status = False if self.status == 3 else True
            chess_coord = deepcopy(self.chess_coord)
            blank = self.blank
            settings = []
            settings.append(int(self.settings.value('child_num', 2300)))
            settings.append(int(self.settings.value('node_num', 200000)))
            settings.append(float(self.settings.value('UCB_COEF', 1.0)))
            settings.append(int(self.settings.value('simulate', 1)))
            settings.append(int(self.settings.value('min_visit_num', 30)))
            settings.append(int(self.settings.value('max_visit_num', 1000000)))
            settings.append(int(self.settings.value('process_num', 3)))
            settings.append(float(self.settings.value('virtual', 2.0)))
            pack = []
            pack.append(chessboard)
            pack.append(status)
            pack.append(chess_coord)
            pack.append(blank)
            pack.append(mode)
            pack.append(ip_pack)
            pack.append(settings)
            pack.append(compute_port)
            zip = dumps(pack)
            # print('zip:%d'%sys.getsizeof(zip.encode(encoding='utf-8')))
            local.sendto(zip.encode(encoding='utf-8'), (host, port))

            counter = Count_time(self, local, (host, port))
            counter.start()

            data, address = local.recvfrom(2048)
            if self.stop_flag == True:
                self.stop_flag = False

            local.close()
            return list(loads(data.decode(encoding='utf-8')))
            # try:
            #     status=False if self.status==3 else True
            #     for i, j in zip([0] * 11, range(11)):
            #         self.chessboard[(i, j)] = 1
            #         self.chessboard[(11 - i, 11 - j)] = 1
            #         self.chessboard[(j, 11)] = 1
            #         self.chessboard[(11 - j, 0)] = 1
            #     si=Simulator(self.chessboard,status,self.chess_coord,1)
            #     si.chessMove(self.chessboard,status,self.chess_coord)
            #     return si.result
            # except Exception as e:
            #     print(e)
        except Exception as e:
            print(e)

    '''
    以下为主线程UI逻辑函数
    '''

    def start_game(self):
        try:
            if self.mode == 2 or self.mode == 3:
                self.start_flag = True
            if self.run_status == 1 or self.run_status == 0:
                self.initBoard()
                self.white_time.setText("正方：  00:00  ")
                self.black_time.setText("反方：  00:00  ")
                self.game_eva.setText("估值：  0.0  ")
                self.action.setText("  None  ")
                for i in range(2):
                    self.time_counter[i].setHMS(0, 0, 0)
                self.run_status = 0
            self.antimouse = 0
            self.start.setEnabled(False)
            self.pause.setEnabled(True)
            self.stop.setEnabled(True)
            self.Situation.setEnabled(True)
            self.open.setEnabled(False)
            self.save.setEnabled(True)
            self.Set.setEnabled(False)

            self.m_new_game.setEnabled(False)
            self.m_pause_game.setEnabled(True)
            self.m_stop_game.setEnabled(True)
            self.m_history.setEnabled(True)
            self.m_open.setEnabled(False)
            self.m_save.setEnabled(True)
            self.m_aspect.setEnabled(False)
            self.m_mode.setEnabled(False)
            self.m_parameter.setEnabled(False)
            self.m_function.setEnabled(False)
            self.game_status.setText("游戏状态：  运行中  ")
            if self.status == 1 or self.status == 3:
                self.time_recorder[0].start(1000)
            else:
                self.time_recorder[1].start(1000)

        except Exception as e:
            print(e)

    def pause_game(self):
        if self.status == 3 or self.status == 4:
            QMessageBox.warning(self, '提示', '当前为电脑落子，不允许暂停！', QMessageBox.Yes, QMessageBox.Yes)
            return
        self.antimouse = 1
        self.run_status = 2
        self.start.setEnabled(True)
        self.pause.setEnabled(False)
        self.m_new_game.setEnabled(True)
        self.m_pause_game.setEnabled(False)
        for i in range(2):
            if self.time_recorder[i].isActive() == True:
                self.time_recorder[i].stop()
        self.game_status.setText("游戏状态：  已暂停  ")

    def stop_game(self):
        if self.status == 3 or self.status == 4:
            QMessageBox.warning(self, '提示', '当前为电脑落子，不允许停止，请使用强制落子功能！', QMessageBox.Yes, QMessageBox.Yes)
            return
        self.run_status = 1
        self.antimouse = 1
        self.start_flag = False
        self.stop.setEnabled(False)
        self.pause.setEnabled(False)
        self.start.setEnabled(True)
        self.Situation.setEnabled(False)
        self.open.setEnabled(True)
        self.Set.setEnabled(True)

        self.m_stop_game.setEnabled(False)
        self.m_pause_game.setEnabled(False)
        self.m_new_game.setEnabled(True)
        self.m_history.setEnabled(False)
        self.m_open.setEnabled(True)
        self.m_aspect.setEnabled(True)
        self.m_mode.setEnabled(True)
        self.m_parameter.setEnabled(True)
        self.m_function.setEnabled(True)

        for i in range(2):
            if self.time_recorder[i].isActive() == True:
                self.time_recorder[i].stop()
        self.game_status.setText("游戏状态：  已停止  ")
        self.openflag = 0

    def update_time1(self):
        self.time_counter[0] = self.time_counter[0].addSecs(1)
        temp = self.time_counter[0].toString('mm:ss')
        self.white_time.setText("正方：  %s  " % temp)

    def update_time2(self):
        self.time_counter[1] = self.time_counter[1].addSecs(1)
        temp = self.time_counter[1].toString('mm:ss')
        self.black_time.setText("反方：  %s  " % temp)

    def return_begin(self):
        try:
            moves = self.gamerecord.getLastAllStep()
            for result in moves:
                # print(result)
                self.change_status()
                self.cancel_move(result[0], result[1], result[2], result[3], result[4], result[5])

            if len(self.gamerecord.gameForwardStack) == 0:
                self.set_left_disable()
            self.set_right_enable()
            pass
        except Exception as e:
            print(e)

    def back_five(self):
        try:
            moves = self.gamerecord.getLastFiveStep()
            for result in moves:
                self.change_status()
                self.cancel_move(result[0], result[1], result[2], result[3], result[4], result[5])

            if len(self.gamerecord.gameForwardStack) == 0:
                self.set_left_disable()
            self.set_right_enable()
            pass
        except Exception as e:
            print(e)

    def back(self):
        try:
            result = self.gamerecord.getLastStep()
            self.change_status()
            self.cancel_move(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])

            if len(self.gamerecord.gameForwardStack) == 0:
                self.set_left_disable()
            self.set_right_enable()
            pass
        except Exception as e:
            print(e)

    def forward(self):
        try:
            result = self.gamerecord.getNextStep()
            self.change_status()
            self.conduct_move(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])

            if len(self.gamerecord.gameBackwardStack) == 0:
                self.set_right_disable()
            self.set_left_enable()
            pass
        except Exception as e:
            print(e)

    def forward_five(self):
        try:
            moves = self.gamerecord.getNextFiveStep()
            for result in moves:
                self.change_status()
                self.conduct_move(result[0], result[1], result[2], result[3], result[4], result[5])

            if len(self.gamerecord.gameBackwardStack) == 0:
                self.set_right_disable()
            self.set_left_enable()
            pass
        except Exception as e:
            print(e)

    def return_end(self):
        try:
            moves = self.gamerecord.getNextAllStep()
            for result in moves:
                self.change_status()
                self.conduct_move(result[0], result[1], result[2], result[3], result[4], result[5])

            if len(self.gamerecord.gameBackwardStack) == 0:
                self.set_right_disable()
            self.set_left_enable()
            pass
        except Exception as e:
            print(e)

    def cancel_move(self, last_x, last_y, x, y, arr_x, arr_y):
        offset = self.chess.width() / 12
        list = self.chess.childAt(QPoint(arr_x * offset + 2, (11 - arr_y) * offset + 2))
        self.chessboard[(arr_x, arr_y)] = 0
        list.setVisible(False)
        self.labelList_used.remove(list)
        self.labelList.append(list)
        chess1 = self.chess.childAt(QPoint(x * offset + 2, (11 - y) * offset + 2))
        flag = self.chessboard[(x, y)]
        if flag == 2:
            self.chess_coord[0].remove((x, y))
            self.chess_coord[0].append((last_x, last_y))
        else:
            self.chess_coord[1].remove((x, y))
            self.chess_coord[1].append((last_x, last_y))
        chess1.setGeometry(last_x * offset + 2, (11 - last_y) * offset + 2, offset - 2, offset - 2)
        chess1.setProperty("coordx", last_x)
        chess1.setProperty("coordy", last_y)
        self.chessboard[(last_x, last_y)] = flag
        self.chessboard[(x, y)] = 0
        self.blank += 1
        self.clicktimes -= 3
        pass

    def conduct_move(self, last_x, last_y, x, y, arr_x, arr_y):
        flag = self.chessboard[(last_x, last_y)]
        self.chessboard[(x, y)] = flag
        self.chessboard[(last_x, last_y)] = 0
        offset = self.chess.width() / 12
        chess1 = self.chess.childAt(QPoint(last_x * offset + 2, (11 - last_y) * offset + 2))
        if flag == 2:
            self.chess_coord[0].remove((last_x, last_y))
            self.chess_coord[0].append((x, y))
        else:
            self.chess_coord[1].remove((last_x, last_y))
            self.chess_coord[1].append((x, y))
        chess1.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
        chess1.setProperty("coordx", x)
        chess1.setProperty("coordy", y)

        list = self.labelList.pop()
        list.setVisible(True)
        list.setPixmap(QPixmap('./images/obstacle.png'))
        list.setGeometry(arr_x * offset + 2, (11 - arr_y) * offset + 2, offset - 2, offset - 2)
        list.setProperty("coordx", arr_x)
        list.setProperty("coordy", arr_y)
        self.labelList_used.append(list)
        self.chessboard[(arr_x, arr_y)] = 1

        self.blank -= 1
        self.clicktimes += 3
        pass

    def change_status(self):
        self.antiThreadFlag = 1
        if self.mode == 1:
            self.status = 3 - self.status
            self.antimouse = 0
            self.Refresh.setEnabled(False)
            self.m_refresh.setEnabled(False)
        elif self.mode == 2:
            if self.status == 1 or self.status == 2:
                self.status = 5 - self.status
                self.antimouse = 1
                self.Refresh.setEnabled(True)
                self.m_refresh.setEnabled(True)
            elif self.status == 3 or self.status == 4:
                self.status = 5 - self.status
                self.antimouse = 0
                self.Refresh.setEnabled(False)
                self.m_refresh.setEnabled(False)
        elif self.mode == 3:
            self.status = 7 - self.status
            self.antimouse = 1
            self.Refresh.setEnabled(True)
            self.m_refresh.setEnabled(True)

        if self.time_recorder[0].isActive() == True:
            self.time_recorder[0].stop()
            self.time_recorder[1].start(1000)
        else:
            self.time_recorder[1].stop()
            self.time_recorder[0].start(1000)

    def set_left_enable(self):
        self.Hide_left_left.setEnabled(True)
        self.Hide_left.setEnabled(True)
        self.left.setEnabled(True)
        self.m_up.setEnabled(True)
        self.m_up5.setEnabled(True)
        self.m_start.setEnabled(True)

    def set_right_enable(self):
        self.Hide_right_right.setEnabled(True)
        self.Hide_right.setEnabled(True)
        self.right.setEnabled(True)
        self.m_down.setEnabled(True)
        self.m_down5.setEnabled(True)
        self.m_end.setEnabled(True)

    def set_left_disable(self):
        self.Hide_left_left.setEnabled(False)
        self.Hide_left.setEnabled(False)
        self.left.setEnabled(False)
        self.m_up.setEnabled(False)
        self.m_up5.setEnabled(False)
        self.m_start.setEnabled(False)

    def set_right_disable(self):
        self.Hide_right_right.setEnabled(False)
        self.Hide_right.setEnabled(False)
        self.right.setEnabled(False)
        self.m_down.setEnabled(False)
        self.m_down5.setEnabled(False)
        self.m_end.setEnabled(False)

    def release_thread(self):
        self.antiThreadFlag = 0

    def showText(self):
        if self.situation == None:
            return
        else:
            if self.situation.isVisible() == True:
                self.situation.setVisible(False)
            else:
                self.situation = Situation(self.show_text)
                self.situation.move(self.x() + self.width(), self.y())
                self.situation.setVisible(True)

    def setSituation(self):
        if self.situation == None:
            self.situation = Situation(self.show_text)
        else:
            if self.situation.isVisible() == True:
                self.situation = Situation(self.show_text)
                self.situation.move(self.x() + self.width(), self.y())
                self.situation.setVisible(True)

    def openFile(self):
        openfile = QFileDialog.getOpenFileName(self, '打开棋谱', './chess manual', 'Txt Files(*.txt)')
        if openfile[0] == '':
            return
        with open(openfile[0], 'r', encoding='utf-8') as f:
            text = f.read()
            self.string_to_chessboard(text)
        self.openflag = 1

    def saveFile(self):
        savefile = QFileDialog.getSaveFileName(self, '保存棋谱', './chess manual', 'Txt Files(*.txt)')
        if savefile[0] == '':
            return
        with open(savefile[0], 'w', encoding='utf-8') as f:
            text = self.chessboard_to_string()
            f.write(text)

    def string_to_chessboard(self, text):
        text = text.split('\n')

        for i in range(2):
            self.chess_coord[i].clear()
        self.gamerecord.gameForwardStack.clear()
        self.gamerecord.gameBackwardStack.clear()

        n = 0
        temp = text[len(text) - 4]
        for i in range(1, 11):
            for j in range(1, 11):
                self.chessboard[(i, j)] = int(temp[n])
                n += 1

        n = 0
        temp = text[len(text) - 3]
        for i in range(2):
            for j in range(4):
                self.chess_coord[i].append((int(temp[n:n + 2]), int(temp[n + 2:n + 4])))
                n += 4

        n = 0
        temp = text[len(text) - 2]
        while n < len(temp):
            collect = []
            for i in range(0, 12, 2):
                collect.append(int(temp[n + i:n + i + 2]))
            self.gamerecord.gameForwardStack.append(tuple(collect))
            n += 12

        n = 0
        temp = text[len(text) - 1]
        while n < len(temp):
            collect = []
            for i in range(0, 12, 2):
                collect.append(int(temp[n + i:n + i + 2]))
            self.gamerecord.gameBackwardStack.append(tuple(collect))
            n += 12
        pass

    def chessboard_to_string(self):
        string = '< 亚 马 逊 棋 游 戏----------棋 谱 记 录 >\n\n'
        string += '< 基 本 游 戏 信 息 ↓ >\n\n'
        string += QDateTime.currentDateTime().toString('记录时间： yyyy/MM/dd  hh:mm:ss\n\n')
        string += '正方：%s    已用时间：%s\n\n' % (self.plus, self.time_counter[0].toString('mm:ss'))
        string += '反方：%s    已用时间：%s\n\n' % (self.minus, self.time_counter[1].toString('mm:ss'))
        string += '< 基 本 游 戏 信 息 ↑ >\n\n'
        string += '< 行 棋 记 录 ↓ >\n\n'
        char = '-ABCDEFGHIJ-'
        for record in self.gamerecord.gameForwardStack:
            string += ' ' + char[record[0]] + '%2d' % (record[1]) + ' → ' + char[record[2]] + '%2d' % (
                record[3]) + ' → ' + \
                      char[record[4]] + '%2d' % (record[5]) + '\n\n'
        string += '< 行 棋 记 录 ↑ >\n\n'
        string += '< 棋 盘 数 据 ↓ >\n\n'
        string += '   -----------------------------------------\n'
        for i in range(1, 11):
            string += '%2d | ' % i
            for j in range(1, 11):
                string += str(self.chessboard[(j, 11 - i)]) + ' | '
            string += '\n'
            string += '   -----------------------------------------\n'
        string += '     A   B   C   D   E   F   G   H   I   J   \n\n'
        string += '< 棋 盘 数 据 ↑ >\n\n'
        string += '< 棋 盘 存 储 ↓ >\n\n'
        for i in range(1, 11):
            for j in range(1, 11):
                string += str(self.chessboard[(i, j)])
        string += '\n'
        for i in range(2):
            for coord in self.chess_coord[i]:
                string += '%2d' % coord[0] + '%2d' % coord[1]
        string += '\n'
        for coord in self.gamerecord.gameForwardStack:
            for i in range(6):
                string += '%2d' % coord[i]
        string += '\n'
        for coord in self.gamerecord.gameBackwardStack:
            for i in range(6):
                string += '%2d' % coord[i]
        return string

    def generate_set(self):
        if self.set_dialog == None:
            self.set_dialog = General()
            screen = QDesktopWidget().screenGeometry()
            size = self.set_dialog.geometry()
            self.set_dialog.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            self.set_dialog.show()
        else:
            if self.set_dialog.isVisible() == True:
                self.set_dialog.setVisible(False)
            else:
                self.set_dialog.setVisible(True)
                self.set_dialog.setCurrentIndex(0)
                self.set_dialog.aspect.start.setEnabled(True)
                self.set_dialog.mode.start.setEnabled(True)
                self.set_dialog.parameter.start.setEnabled(True)
                self.set_dialog.func.start.setEnabled(True)

    def generate_mode(self):
        if self.mode_dialog == None:
            self.mode_dialog = Mode()
            screen = QDesktopWidget().screenGeometry()
            size = self.mode_dialog.geometry()
            self.mode_dialog.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            self.mode_dialog.show()
        else:
            if self.mode_dialog.isVisible() == True:
                self.mode_dialog.setVisible(False)
            else:
                self.mode_dialog.setVisible(True)
                self.mode_dialog.start.setEnabled(True)

    def generate_aspect(self):
        if self.aspect_dialog == None:
            self.aspect_dialog = Aspect()
            screen = QDesktopWidget().screenGeometry()
            size = self.aspect_dialog.geometry()
            self.aspect_dialog.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            self.aspect_dialog.show()
        else:
            if self.aspect_dialog.isVisible() == True:
                self.aspect_dialog.setVisible(False)
            else:
                self.aspect_dialog.setVisible(True)
                self.aspect_dialog.start.setEnabled(True)

    def generate_parameter(self):
        if self.parameter_dialog == None:
            self.parameter_dialog = Parameter()
            screen = QDesktopWidget().screenGeometry()
            size = self.parameter_dialog.geometry()
            self.parameter_dialog.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            self.parameter_dialog.show()
        else:
            if self.parameter_dialog.isVisible() == True:
                self.parameter_dialog.setVisible(False)
            else:
                self.parameter_dialog.setVisible(True)
                self.parameter_dialog.setEnabled(True)

    def generate_function(self):
        if self.function_dialog == None:
            self.function_dialog = Function()
            screen = QDesktopWidget().screenGeometry()
            size = self.function_dialog.geometry()
            self.function_dialog.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            self.function_dialog.show()
        else:
            if self.function_dialog.isVisible() == True:
                self.function_dialog.setVisible(False)
            else:
                self.function_dialog.setVisible(True)
                self.function_dialog.start.setEnabled(True)

    def generate_about(self):
        if self.about_dialog == None:
            self.about_dialog = About()
            screen = QDesktopWidget().screenGeometry()
            size = self.about_dialog.geometry()
            self.about_dialog.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            self.about_dialog.show()
        else:
            if self.about_dialog.isVisible() == True:
                self.about_dialog.setVisible(False)
            else:
                self.about_dialog.setVisible(True)

    # 设置菜单栏
    def menuLayout(self):
        self.bar = self.menuBar()
        # 游戏的子菜单
        game = self.bar.addMenu(" 游  戏 ")
        self.m_new_game = QAction("新游戏", self)
        self.m_new_game.setShortcut("F5")
        self.m_new_game.setIcon(QIcon('./images/Start.png'))
        self.m_new_game.triggered.connect(self.start_game)
        game.addAction(self.m_new_game)
        self.m_pause_game = QAction("暂停游戏", self)
        self.m_pause_game.setShortcut("F6")
        self.m_pause_game.setIcon(QIcon('./images/Pause.png'))
        self.m_pause_game.setEnabled(False)
        self.m_pause_game.triggered.connect(self.pause_game)
        game.addAction(self.m_pause_game)
        self.m_stop_game = QAction("停止游戏", self)
        self.m_stop_game.setShortcut("F7")
        self.m_stop_game.setIcon(QIcon('./images/Stop_red.png'))
        self.m_stop_game.setEnabled(False)
        self.m_stop_game.triggered.connect(self.stop_game)
        game.addAction(self.m_stop_game)
        game.addSeparator()
        self.m_open = QAction("打开", self)
        self.m_open.setShortcut("Ctrl+O")
        self.m_open.setIcon(QIcon('./images/open_file.png'))
        self.m_open.triggered.connect(self.openFile)
        game.addAction(self.m_open)
        self.m_save = QAction("保存", self)
        self.m_save.setShortcut("Ctrl+S")
        self.m_save.setIcon(QIcon('./images/Save.png'))
        self.m_save.setEnabled(False)
        self.m_save.triggered.connect(self.saveFile)
        game.addAction(self.m_save)
        game.addSeparator()
        self.m_quit = QAction("退出", self)
        self.m_quit.setShortcut("Ctrl+Q")
        self.m_quit.setIcon(QIcon('./images/quit.png'))
        self.m_quit.triggered.connect(self.close)
        game.addAction(self.m_quit)
        # 棋局控制的子菜单
        situation = self.bar.addMenu("棋局控制")
        self.m_up = QAction("后退一步", self)
        self.m_up.setShortcut("F9")
        self.m_up.setIcon(QIcon('./images/left.png'))
        self.m_up.triggered.connect(self.back)
        situation.addAction(self.m_up)
        self.m_down = QAction("前进一步", self)
        self.m_down.setShortcut("F10")
        self.m_down.setIcon(QIcon('./images/right.png'))
        self.m_down.triggered.connect(self.forward)
        situation.addAction(self.m_down)
        self.m_up5 = QAction("后退五步", self)
        self.m_up5.setShortcut("F11")
        self.m_up5.setIcon(QIcon('./images/Hide_left.png'))
        self.m_up5.triggered.connect(self.back_five)
        situation.addAction(self.m_up5)
        self.m_down5 = QAction("前进五步", self)
        self.m_down5.setShortcut("F12")
        self.m_down5.setIcon(QIcon('./images/Hide_right.png'))
        self.m_down5.triggered.connect(self.forward_five)
        situation.addAction(self.m_down5)
        self.m_start = QAction("回到开局", self)
        self.m_start.setShortcut("F1")
        self.m_start.setIcon(QIcon('./images/Hide_left_left.png'))
        self.m_start.triggered.connect(self.return_begin)
        situation.addAction(self.m_start)
        self.m_end = QAction("直达终局", self)
        self.m_end.setShortcut("F2")
        self.m_end.setIcon(QIcon('./images/Hide_right_right.png'))
        self.m_end.triggered.connect(self.return_end)
        situation.addAction(self.m_end)
        situation.addSeparator()
        self.m_move_now = QAction("强制落子", self)
        self.m_move_now.setShortcut("Ctrl+I")
        self.m_move_now.setIcon(QIcon('./images/Prohibit.png'))
        self.m_move_now.setEnabled(False)
        self.m_move_now.triggered.connect(self.moveInforce)
        situation.addAction(self.m_move_now)
        self.m_refresh = QAction('释放线程', self)
        self.m_refresh.setShortcut("Ctrl+R")
        self.m_refresh.setIcon(QIcon('./images/Refresh.png'))
        self.m_refresh.setEnabled(False)
        self.m_refresh.triggered.connect(self.release_thread)
        situation.addAction(self.m_refresh)

        # 设置的子菜单
        setting = self.bar.addMenu(" 设  置 ")
        self.m_mode = QAction("对战模式", self)
        self.m_mode.triggered.connect(self.generate_mode)
        self.m_mode.setShortcut("Ctrl+M")
        setting.addAction(self.m_mode)
        self.m_aspect = QAction("界面设置", self)
        self.m_aspect.setShortcut("Ctrl+P")
        self.m_aspect.triggered.connect(self.generate_aspect)
        setting.addAction(self.m_aspect)
        setting.addSeparator()
        self.m_function = QAction("功能分配", self)
        self.m_function.setShortcut("Ctrl+F")
        self.m_function.triggered.connect(self.generate_function)
        setting.addAction(self.m_function)
        self.m_parameter = QAction("参数设置", self)
        self.m_parameter.triggered.connect(self.generate_parameter)
        self.m_parameter.setShortcut("Ctrl+H")
        setting.addAction(self.m_parameter)
        # 视图的子菜单
        view = self.bar.addMenu(" 视  图 ")
        self.toolcolumn = QAction("工具栏", self)
        self.toolcolumn.setShortcut("Ctrl+T")
        self.toolcolumn.setIcon(QIcon("./images/checked.png"))
        self.toolcolumn.triggered.connect(self.displayToolbar)
        view.addAction(self.toolcolumn)
        self.m_history = QAction("博弈实况", self)
        self.m_history.setIcon(QIcon('./images/Situation.png'))
        self.m_history.setEnabled(False)
        self.m_history.triggered.connect(self.showText)
        view.addAction(self.m_history)
        self.m_info = QAction("关于moonlight", self)
        self.m_info.setShortcut("Ctrl+A")
        self.m_info.setIcon(QIcon('./images/temp.png'))
        self.m_info.triggered.connect(self.generate_about)
        view.addAction(self.m_info)

    # 设置工具栏
    def toolLayout(self):
        self.tb = QToolBar()
        self.tb.setObjectName("tb")
        self.start = QAction(QIcon("./images/Start.png"), "开始&继续", self)
        self.start.triggered.connect(self.start_game)
        self.tb.addAction(self.start)
        self.pause = QAction(QIcon("./images/Pause.png"), "暂停", self)
        self.pause.triggered.connect(self.pause_game)
        self.pause.setEnabled(False)
        self.tb.addAction(self.pause)
        self.stop = QAction(QIcon("./images/Stop_red.png"), "停止", self)
        self.stop.triggered.connect(self.stop_game)
        self.stop.setEnabled(False)
        self.tb.addAction(self.stop)
        self.tb.addSeparator()
        self.open = QAction(QIcon("./images/open_file.png"), "打开", self)
        self.open.triggered.connect(self.openFile)
        self.tb.addAction(self.open)
        self.save = QAction(QIcon("./images/Save.png"), "保存", self)
        self.save.triggered.connect(self.saveFile)
        self.tb.addAction(self.save)
        self.save.setEnabled(False)
        self.tb.addSeparator()
        self.Hide_left_left = QAction(QIcon("./images/Hide_left_left.png"), "回到开局", self)
        self.Hide_left_left.triggered.connect(self.return_begin)
        self.tb.addAction(self.Hide_left_left)
        self.Hide_left = QAction(QIcon("./images/Hide_left.png"), "后退五步", self)
        self.Hide_left.triggered.connect(self.back_five)
        self.tb.addAction(self.Hide_left)
        self.left = QAction(QIcon("./images/left.png"), "后退一步", self)
        self.left.triggered.connect(self.back)
        self.tb.addAction(self.left)
        self.right = QAction(QIcon("./images/right.png"), "前进一步", self)
        self.right.triggered.connect(self.forward)
        self.tb.addAction(self.right)
        self.Hide_right = QAction(QIcon("./images/Hide_right.png"), "前进五步", self)
        self.Hide_right.triggered.connect(self.forward_five)
        self.tb.addAction(self.Hide_right)
        self.Hide_right_right = QAction(QIcon("./images/Hide_right_right.png"), "直达终局", self)
        self.Hide_right_right.triggered.connect(self.return_end)
        self.tb.addAction(self.Hide_right_right)
        self.tb.addSeparator()
        self.Prohibit = QAction(QIcon("./images/Prohibit.png"), "强制落子", self)
        self.Prohibit.triggered.connect(self.moveInforce)
        self.Prohibit.setEnabled(False)
        self.tb.addAction(self.Prohibit)
        self.Refresh = QAction(QIcon("./images/Refresh.png"), "释放线程", self)
        self.Refresh.setEnabled(False)
        self.Refresh.triggered.connect(self.release_thread)
        self.tb.addAction(self.Refresh)
        self.tb.addSeparator()
        self.Situation = QAction(QIcon("./images/Situation.png"), "博弈实况", self)
        self.Situation.triggered.connect(self.showText)
        self.Situation.setEnabled(False)
        self.tb.addAction(self.Situation)
        self.Set = QAction(QIcon("./images/Setting.png"), "设置", self)
        self.tb.addAction(self.Set)
        self.Set.triggered.connect(self.generate_set)
        # self.tb.addSeparator()
        # Sound = QAction(QIcon("./images/Sound.png"), "声音", self)
        # self.tb.addAction(Sound)
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

    def showLabel(self):

        self.game_time = QLabel(self.centralwidget)
        self.game_time.setFont(QFont("微软雅黑", 15))
        self.game_time.setText("游戏时间————————————————————————————————————————————\
                        ——————————")
        self.game_time.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15 * 4 + 20
                                   , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.white_time = QLabel(self.centralwidget)
        self.white_time.setFont(QFont("微软雅黑", 15))
        self.white_time.setText("正方：  00:00  ")
        self.white_time.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 5 + 20
                                    , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.black_time = QLabel(self.centralwidget)
        self.black_time.setFont(QFont("微软雅黑", 15))
        self.black_time.setText("反方：  00:00  ")
        self.black_time.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 6 + 20
                                    , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.current_action = QLabel(self.centralwidget)
        self.current_action.setFont(QFont("微软雅黑", 15))
        self.current_action.setText("当前行为————————————————————————————————————————————\
                                ——————————")
        self.current_action.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15 * 7 + 40
                                        , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.action = QLabel(self.centralwidget)
        self.action.setFont(QFont("微软雅黑", 15))
        self.action.setText("  None  ")
        self.action.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 8 + 45
                                , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.current_status = QLabel(self.centralwidget)
        self.current_status.setFont(QFont("微软雅黑", 15))
        self.current_status.setText("状态————————————————————————————————————————————\
                                        ——————————")
        self.current_status.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15 * 9 + 60
                                        , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.game_status = QLabel(self.centralwidget)
        self.game_status.setFont(QFont("微软雅黑", 15))
        self.game_status.setText("游戏状态：  等待开始  ")
        self.game_status.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 10 + 60
                                     , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.game_eva = QLabel(self.centralwidget)
        self.game_eva.setFont(QFont("微软雅黑", 15))
        self.game_eva.setText("估值：  0.0  ")
        self.game_eva.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 11 + 60
                                  , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

        self.player = QLabel(self.centralwidget)
        self.player.setFont(QFont("微软雅黑", 15))
        self.player.setText("玩家————————————————————————————————————————————\
                                ——————————")
        self.player.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15
                                , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.white = QLabel(self.centralwidget)
        self.white.setFont(QFont("微软雅黑", 15))
        self.white.setText("正方：  %s  " % self.plus)
        self.white.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 2
                               , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.black = QLabel(self.centralwidget)
        self.black.setFont(QFont("微软雅黑", 15))
        self.black.setText("反方：  %s  " % self.minus)
        self.black.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 3
                               , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)

    # 初始化棋盘
    def initBoard(self):

        self.times = 1
        self.clicktimes = 0
        self.lastx = -1
        self.lasty = -1
        self.blank = 92

        self.status = int(self.settings.value("status", 1))
        self.mode = int(self.settings.value("mode", 1))

        while len(self.labelList_used) != 0:
            element = self.labelList_used.pop()
            element.setVisible(False)
            self.labelList.append(element)

        self.game.over = False
        self.game.winner = -1

        if self.status == 1 or self.status == 2:
            self.antimouse = 0
        else:
            self.antimouse = 1
        # 此处需要加上显示棋子的label的清除
        if self.openflag == 0:
            self.chessboard = {}
            self.chess_coord = []
            self.chess_coord.append([])
            self.chess_coord.append([])
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

        minsize = min(self.centralwidget.width() / 3 * 2 - 40, self.centralwidget.height() - 20)
        self.chess.setGeometry(20, 20, minsize, minsize)
        self.chess.setPixmap(QPixmap("./images/%s" % (str(self.settings.value('chessboard', 'chessboard.png')))))
        self.chess.setScaledContents(True)
        self.show_text = "---------博--弈--实--况---------\n"
        if self.mode == 1:
            self.plus = 'Human'
            self.minus = 'Human'
        elif self.mode == 2:
            if self.status == 1:
                self.plus = 'Human'
                self.minus = 'Computer'
            else:
                self.plus = 'Computer'
                self.minus = 'Human'
        else:
            self.plus = 'Computer'
            self.minus = 'Computer'
        self.show_text += '  正方：  %s  \n' % self.plus
        self.show_text += '  反方：  %s  \n\n' % self.minus
        self.setSituation()

        if self.white!=None and self.black!=None:
            self.white.setText("正方：  %s  " % self.plus)
            self.black.setText("反方：  %s  " % self.minus)

        # 布置棋盘
        offset = self.chess.width() / 12
        for x in range(1, 11):
            for y in range(1, 11):
                if self.chessboard[(x, y)] == 2:
                    la = self.labelList.pop()
                    la.setVisible(True)
                    la.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('plus', 'chess_white')))))
                    la.setScaledContents(True)
                    la.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
                    la.setProperty("coordx", x)
                    la.setProperty("coordy", y)
                    self.labelList_used.append(la)
                elif self.chessboard[(x, y)] == 3:
                    la = self.labelList.pop()
                    la.setVisible(True)
                    la.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('minus', 'chess_black')))))
                    la.setScaledContents(True)
                    la.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
                    la.setProperty("coordx", x)
                    la.setProperty("coordy", y)
                    self.labelList_used.append(la)
                elif self.chessboard[(x, y)] == 1:
                    la = self.labelList.pop()
                    la.setVisible(True)
                    la.setPixmap(QPixmap("./images/obstacle.png"))
                    la.setScaledContents(True)
                    la.setGeometry(x * offset + 2, (11 - y) * offset + 2, offset - 2, offset - 2)
                    la.setProperty("coordx", x)
                    la.setProperty("coordy", y)
                    self.labelList_used.append(la)
                    self.blank -= 1
                    self.clicktimes += 3
        if len(self.gamerecord.gameForwardStack) == 0:
            self.set_left_disable()
        else:
            self.set_left_enable()

        if len(self.gamerecord.gameBackwardStack) == 0:
            self.set_right_disable()
        else:
            self.set_right_enable()

        self.start_flag = True
        if self.mode == 2 or self.mode == 3:
            self.workthread = WorkThread(self)
            self.workthread.returnResult.connect(self.threadConduct)
            self.antiThreadFlag = 0  # 开启子线程响应
            self.workthread.start()

    # 重载窗口大小改变事件
    def resizeEvent(self, event):
        minsize = min(self.centralwidget.width() / 3 * 2 - 40, self.centralwidget.height() - 40)
        self.chess.setGeometry(20, 20, minsize, minsize)
        self.player.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15,
                                self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.white.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 2
                               , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.black.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 3
                               , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.game_time.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15 * 4 + 20
                                   , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.white_time.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 5 + 20
                                    , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.black_time.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 6 + 20
                                    , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.current_action.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15 * 7 + 40
                                        , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.action.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 8 + 45
                                , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.current_status.setGeometry(self.centralwidget.width() / 3 * 2, self.centralwidget.height() / 15 * 9 + 60
                                        , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.game_status.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 10 + 60
                                     , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
        self.game_eva.setGeometry(self.centralwidget.width() / 3 * 2 + 40, self.centralwidget.height() / 15 * 11 + 60
                                  , self.centralwidget.width() / 3 - 40, self.centralwidget.height() / 15)
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
                                list.setPixmap(
                                    QPixmap("./images/%s.png" % (str(self.settings.value('plus', 'chess_white')))))
                            else:
                                list.setPixmap(
                                    QPixmap("./images/%s.png" % (str(self.settings.value('minus', 'chess_black')))))
                            self.action.setText("  None  ")
                            self.clicktimes -= 1

    # 发射障碍动画
    def shootArrow(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        if self.currentChess == 2:
            self.action.setText("  正方(人) 在(%d,%d)处设置障碍   " % (x, y))
            self.show_text += "  正方(人) 在(%d,%d)处设置障碍   \n" % (x, y)
            self.setSituation()
        else:
            self.action.setText("  反方(人) 在(%d,%d)处设置障碍   " % (x, y))
            self.show_text += "  反方(人) 在(%d,%d)处设置障碍   \n" % (x, y)
            self.setSituation()

        ba = self.labelList.pop()

        ba.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('ball', 'ball')))))
        ba.setScaledContents(True)
        ba.setGeometry(lx * offset + 2, (11 - ly) * offset + 2, offset - 2, offset - 2)
        ba.setProperty("coordx", x)
        ba.setProperty("coordy", y)
        ba.setVisible(True)
        self.labelList_used.append(ba)
        self.animation = QPropertyAnimation(ba, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEndValue(QRect(x * offset + 1.5, (11 - y) * offset + 1.5, offset - 2, offset - 2))
        self.ba = ba
        self.animation.start()
        self.animation.finished.connect(self.playMovie)

    # 属性动画结束后播放movie
    def playMovie(self):
        self.movie = QMovie("./images/%s.gif" % (str(self.settings.value('ball', 'ball'))))
        self.ba.setMovie(self.movie)
        self.movie.start()
        self.movie.finished.connect(self.judgeIsover)
        self.movie.finished.connect(self.freeMouse)

    # 判断棋局是否结束
    def judgeIsover(self):
        self.game.isOver(self.chessboard, self.status, self.chess_coord)
        eva = Evaluator(self.chessboard, self.status, self.chess_coord)
        if self.game.over:
            if self.game.winner == 1:
                QMessageBox.information(self, "游戏结束", "反方获胜！  赢%d" % self.game.blank + "子",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            elif self.game.winner == 0:
                QMessageBox.information(self, "游戏结束", "正方获胜！  赢%d" % self.game.blank + "子",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            else:
                QMessageBox.information(self, "游戏结束", "winner不应该为-1,请检查isOver方法！", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            self.antimouse = 1
            self.antiThreadFlag = 1
            if self.mode == 1:
                self.status = 3 - self.status
            elif self.mode == 2:
                if self.status == 1 or self.status == 2:
                    self.status = 5 - self.status
                elif self.status == 3 or self.status == 4:
                    self.status = 5 - self.status
            elif self.mode == 3:
                self.status = 7 - self.status
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
        if self.time_recorder[0].isActive() == True:
            self.time_recorder[0].stop()
            self.time_recorder[1].start(1000)
        else:
            self.time_recorder[1].stop()
            self.time_recorder[0].start(1000)

        self.game_eva.setText("  估值：%.2f  " % (eva.value))
        self.show_text += "  估值：%.2f  \n\n" % (eva.value)
        self.setSituation()

    # 动画播放时禁止鼠标操作
    def freeMouse(self):
        self.antimouse = 0

    # 棋子移动动画
    def chessMove(self, lx, ly, x, y):
        offset = self.chess.width() / 12
        list = self.chess.childAt(QPoint(lx * offset + 2, (11 - ly) * offset + 2))
        if self.currentChess == 2:
            list.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('plus', 'chess_white')))))
            self.action.setText("  正方(人) 从(%d,%d)移至(%d,%d)   " % (lx, ly, x, y))
            self.show_text += "  正方(人) 从(%d,%d)移至(%d,%d)   \n" % (lx, ly, x, y)
            self.setSituation()
        else:
            list.setPixmap(QPixmap("./images/%s.png" % (str(self.settings.value('minus', 'chess_black')))))
            self.action.setText("  反方(人) 从(%d,%d)移至(%d,%d)   " % (lx, ly, x, y))
            self.show_text += "  反方(人) 从(%d,%d)移至(%d,%d)   \n" % (lx, ly, x, y)
            self.setSituation()

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
            movie = QMovie("./images/%s.gif" % (str(self.settings.value('plus', 'chess_white'))))
            self.action.setText("  正方(人) 选中(%d,%d)处棋子  " % (x, y))
        else:
            movie = QMovie("./images/%s.gif" % (str(self.settings.value('minus', 'chess_black'))))
            self.action.setText("  反方(人) 选中 (%d,%d)处棋子  " % (x, y))
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
                    self.set_left_enable()
                    self.set_right_disable()
                    self.gamerecord.clear_history()
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
                    self.gamerecord.currentMove.append(lx)
                    self.gamerecord.currentMove.append(ly)
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
                    self.selectChess(x, y)
                    pass
                elif self.status == 2 and self.chessboard[(x, y)] == 3:
                    self.currentChess = 3
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

    # 强制落子
    def moveInforce(self):
        self.stop_flag = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/moon_128px.ico"))
    form = InterFace()
    form.show()
    sys.exit(app.exec())
