# -*- coding: utf-8 -*-

# @time： 2018/4/5
# @author: RuiQing Chen
# @definition:

import ctypes
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from socket import socket, AF_INET, SOCK_DGRAM
from json import dumps, loads
from strategy import Strategy
from threading import Thread
from time import sleep


class Child(Thread):
    def __init__(self, work, host, port):
        super(Child, self).__init__()
        self.work = work
        self.host = host
        self.port = port

    def run(self):
        while True:
            data, address = self.work.server.recvfrom(2048)
            print("success!")
            stock = loads(data.decode(encoding='utf-8'))
            if stock[4] == 0:
                self.work.state1.setText("通信中")
                if (len(stock[5])) == 0:
                    QMessageBox.warning(self.work, "提示", "目标IP为空！", QMessageBox.Yes,
                                        QMessageBox.Yes)
                else:
                    # QMessageBox.information(self.work, "提示", "成功传入！", QMessageBox.Yes,
                    #                         QMessageBox.Yes)
                    for i in range(4):
                        print(stock[i])
                pack = []
                pack.append(stock[0])
                pack.append(stock[1])
                pack.append(stock[2])
                pack.append(stock[3])
                pack.append(1)
                pack.append("")
                pack.append(stock[6])
                for ip in stock[5]:
                    self.work.server.sendto(dumps(pack).encode(encoding='utf-8'), (ip, 12306))
                data1, address1 = self.work.server.recvfrom(2048)
                if data1.decode(encoding='utf-8') == 'stop':
                    for ip in stock[5]:
                        self.work.server.sendto('stop'.encode(encoding='utf-8'), (ip, 12306))
                    result = []
                    for i in range(len(stock[5])):
                        data2, address2 = self.work.server.recvfrom(30 * 2048)
                        result.append(loads(data2.decode(encoding='utf-8')))
                    lastResult = self.work.compose(result, len(stock[5]))
                    self.work.server.sendto(dumps(lastResult).encode(encoding='utf-8'), address)
                self.work.state1.setText("未分配")

            if stock[4] == 1:
                self.work.state1.setText("计算中")
                self.work.convert(stock[0])
                strategy = Strategy(self.work.chessboard, stock[1], stock[2], stock[3], stock[6][1], stock[6][2],
                                    stock[6][3], stock[6][4], stock[6][5], stock[6][6], stock[6][7])
                strategy.search_init()
                strategy.search_start()
                while True:
                    data3, address3 = self.work.server.recvfrom(2048)
                    if data3.decode(encoding='utf-8') == 'stop':
                        strategy.search_stop()
                        break
                    else:
                        continue
                strategy.get_all_children()
                self.work.server.sendto(dumps(strategy.children).encode(encoding='utf-8'), address)
                self.work.state1.setText("未分配")


class Assistant(Thread):
    def __init__(self, work, host, port):
        super(Assistant, self).__init__()
        self.work = work
        self.host = host
        self.port = port

    def run(self):
        child = Child(self.work, self.host, self.port)
        child.start()
        while True:
            if self.work.isStop == True:
                self.work.isStop = False
                break
            sleep(0.5)


class Server(QMainWindow):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.setFixedSize(540, 350)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("moonlight----server mode")
        self.runFlag = 0
        self.display()
        self.isStop = False
        self.server = None
        # self.setVolume(30)
        self.center()

    def display(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.tips1 = QLabel(self.centralwidget)
        self.tips1.setFont(QFont("微软雅黑", 18))
        self.tips1.setText("请输入端口号：")
        self.tips1.setGeometry(50, 100, 160, 30)
        self.input1 = QLineEdit(self.centralwidget)
        self.input1.setGeometry(240, 103, 250, 30)
        self.input1.setFont(QFont("微软雅黑", 18))

        self.start = QPushButton(self.centralwidget)
        self.start.setFont(QFont("黑体", 20))
        self.start.setText("启动")
        self.start.setGeometry(80, 220, 150, 50)
        self.start.clicked.connect(self.startListen)

        self.stop = QPushButton(self.centralwidget)
        self.stop.setFont(QFont("黑体", 20))
        self.stop.setText("终止")
        self.stop.setGeometry(310, 220, 150, 50)
        self.stop.clicked.connect(self.stopListen)

        self.state_tip = QLabel(self.centralwidget)
        self.state_tip.setFont(QFont("楷体", 12))
        self.state_tip.setText("状态：")
        self.state_tip.setGeometry(400, 290, 50, 20)

        self.state = QLabel(self.centralwidget)
        self.state.setFont(QFont("楷体", 12))
        self.state.setText("就绪")
        self.state.setGeometry(450, 290, 70, 20)

        self.state_tip1 = QLabel(self.centralwidget)
        self.state_tip1.setFont(QFont("楷体", 12))
        self.state_tip1.setText("当前功能：")

        self.state_tip1.setGeometry(368, 320, 80, 20)
        self.state1 = QLabel(self.centralwidget)
        self.state1.setFont(QFont("楷体", 12))
        self.state1.setText("未分配")
        self.state1.setGeometry(450, 320, 70, 20)

    def startListen(self):
        if self.runFlag == 0:
            if self.input1.text() == "":

                QMessageBox.warning(self, "警告", "端口号不能为空！", QMessageBox.Yes,
                                    QMessageBox.Yes)
                return
            else:
                flag = self.easyCheck(self.input1.text())
                if flag != 5:
                    if flag == 3:
                        QMessageBox.warning(self, "警告", "端口号格式不正确！", QMessageBox.Yes,
                                            QMessageBox.Yes)
                    elif flag == 4:
                        QMessageBox.warning(self, "警告", "端口号应在1025-65535之间！", QMessageBox.Yes,
                                            QMessageBox.Yes)
                    return

            self.state.setText("监听中...")
            self.runFlag = 1
            self.run_socket(int(self.input1.text()))
        else:
            QMessageBox.warning(self, "提示", "该服务器已启动，请勿重复操作！", QMessageBox.Yes,
                                QMessageBox.Yes)

    def run_socket(self, port):
        try:
            host = ''
            if self.server is None:
                self.server = socket(AF_INET, SOCK_DGRAM)
                self.server.bind((host, port))
                self.saveport = port
            else:
                if self.saveport != port:
                    self.server.close()
                    self.server = socket(AF_INET, SOCK_DGRAM)
                    self.server.bind((host, port))
            self.assistant = Assistant(self, host, port)
            self.assistant.start()
        except Exception as e:
            print(e)

    def convert(self, temp):
        self.chessboard = {}
        for i in range(10):
            for j in range(10):
                self.chessboard[(i + 1, j + 1)] = temp[i][j]

    def compose(self, result, num):
        if num > 1:
            for i in range(1, num):
                for j in range(len(result[i])):
                    result[0][j][6] += result[i][j][6]
                    result[0][j][7] += result[i][j][7]
        answer = 0
        maxvalue = -1
        for i in range(len(result[0])):
            if result[0][i][7] != 0:
                temp = result[0][i][6] / result[0][i][7]
                if temp > maxvalue:
                    maxvalue = temp
                    answer = i
        return result[0][answer][0:6]

    def stopListen(self):
        if self.runFlag == 1:
            self.runFlag = 0

            self.isStop = True
            self.state.setText("已终止。")
            self.state1.setText("未分配")
        else:
            QMessageBox.warning(self, "提示", "该服务器未启动，无需终止！", QMessageBox.Yes,
                                QMessageBox.Yes)

    def easyCheck(self, s2):
        for i in range(len(s2)):
            if s2[i] >= '0' and s2[i] <= '9':
                continue
            else:
                return 3
        x = int(s2)
        if x > 1024 and x <= 65535:
            return 5
        else:
            return 4

    def setVolume(self, volume):
        waveOutGetVolume = (ctypes.windll.winmm.waveOutGetVolume)
        waveOutSetVolume = (ctypes.windll.winmm.waveOutSetVolume)
        MINIMUM_VOLUME = 0
        MAXIMUM_VOLUME = 4294967295
        x = volume / 100 * MAXIMUM_VOLUME
        waveOutSetVolume(0, int(x))

    # 将窗口移至屏幕中心
    def center(self):
        # 获取屏幕坐标数据
        screen = QDesktopWidget().screenGeometry()
        # 获取调用对象的坐标数据
        size = self.geometry()
        # 移动作用于调用对象的中心位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/moon_128px.ico"))
    form = Server()
    form.show()
    sys.exit(app.exec())
