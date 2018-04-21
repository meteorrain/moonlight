# -*- coding: utf-8 -*-
# @time： 2018/4/8
# @author: RuiQing Chen
# @definition:

import sys
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Function(QWidget):
    def __init__(self, parent=None):
        super(Function, self).__init__(parent)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setFixedSize(600, 570)
        self.setWindowTitle("分布式系统设置")
        self.settings = QSettings("configure", QSettings.IniFormat)
        self.display()
        self.center()

    def display(self):
        self.line = QLabel(self)
        self.line.setPixmap(QPixmap("./images/black.png"))
        self.line.setScaledContents(True)
        self.line.setGeometry(10, 90, 580, 3)
        self.tips = QLabel(self)
        self.tips.setFont(QFont("楷体", 18))
        self.tips.setText("通信端口号：")
        self.tips.setGeometry(50, 40, 160, 30)
        self.input = QLineEdit(self)
        self.input.setGeometry(240, 40, 250, 30)
        self.input.setFont(QFont("微软雅黑", 15))
        self.input.setText(str(self.settings.value("port", "")))

        self.tips1 = QLabel(self)
        self.tips1.setFont(QFont("楷体", 18))
        self.tips1.setText("通信服务器IP：")
        self.tips1.setGeometry(50, 120, 160, 30)
        self.input1 = QLineEdit(self)
        self.input1.setGeometry(240, 120, 250, 30)
        self.input1.setFont(QFont("微软雅黑", 15))
        self.input1.setText(str(self.settings.value("communicate", "")))

        self.line1 = QLabel(self)
        self.line1.setPixmap(QPixmap("./images/grey.png"))
        self.line1.setScaledContents(True)
        self.line1.setGeometry(10, 170, 580, 3)

        self.line2 = QLabel(self)
        self.line2.setPixmap(QPixmap("./images/black.png"))
        self.line2.setScaledContents(True)
        self.line2.setGeometry(10, 250, 580, 3)
        self.tips3 = QLabel(self)
        self.tips3.setFont(QFont("楷体", 18))
        self.tips3.setText("计算端口号：")
        self.tips3.setGeometry(50, 200, 160, 30)
        self.input2 = QLineEdit(self)
        self.input2.setGeometry(240, 200, 250, 30)
        self.input2.setFont(QFont("微软雅黑", 15))
        self.input2.setText(str(self.settings.value("compute_port", "")))

        self.tips2 = QLabel(self)
        self.tips2.setFont(QFont("楷体", 18))
        self.tips2.setText("计算集群数量：")
        self.tips2.setGeometry(50, 270, 160, 30)
        self.combo2 = QComboBox(self)
        self.combo2.addItems(['  1  ', '  2  ', '  3  '])
        self.combo2.setGeometry(240, 270, 100, 30)
        self.combo2.setFont(QFont("宋体", 15))
        self.combo2.setCurrentIndex(int(self.settings.value('computer_num', 1)) - 1)
        self.combo2.currentIndexChanged.connect(self.changeInputLine)

        self.line1 = QLabel(self)
        self.line1.setPixmap(QPixmap("./images/b4.png"))
        self.line1.setScaledContents(True)
        self.line1.setGeometry(10, 480, 585, 20)

        self.start = QPushButton(self)
        self.start.setFont(QFont("黑体", 15))
        self.start.setText("应用")
        self.start.setGeometry(320, 510, 100, 30)
        self.start.clicked.connect(self.apply)

        self.stop = QPushButton(self)
        self.stop.setFont(QFont("黑体", 15))
        self.stop.setText("退出")
        self.stop.setGeometry(450, 510, 100, 30)
        self.stop.clicked.connect(self.quit)
        self.collect = [[], []]
        for i in range(3):
            x = QLabel(self)
            x.setFont(QFont("楷体", 18))
            self.collect[0].append(x)
            y = QLineEdit(self)
            y.setFont(QFont("微软雅黑", 15))
            self.collect[1].append(y)
        self.changeInputLine()

    def changeInputLine(self):
        for i in range(3):
            self.collect[0][i].setVisible(False)
            self.collect[1][i].setVisible(False)
        if self.combo2.currentIndex() == 0:
            num = 1
        elif self.combo2.currentIndex() == 1:
            num = 2
        elif self.combo2.currentIndex() == 2:
            num = 3
        else:
            num = 0
        for i in range(1, num + 1):
            tips1 = self.collect[0][i - 1]
            tips1.setVisible(True)
            # tips1.setFont(QFont("楷体", 18))
            if i == 1:
                tips1.setText("计算服务器①IP：")
            elif i == 2:
                tips1.setText("计算服务器②IP：")
            else:
                tips1.setText("计算服务器③IP：")
            tips1.setGeometry(50, 320 + (i - 1) * 50, 200, 30)
            input1 = self.collect[1][i - 1]
            input1.setVisible(True)
            input1.setGeometry(240, 320 + (i - 1) * 50, 250, 30)
            # input1.setFont(QFont("微软雅黑", 15))
            input1.setText(self.settings.value("compute%d" % (i - 1), ""))

    # 将窗口移至屏幕中心
    def center(self):
        # 获取屏幕坐标数据
        screen = QDesktopWidget().screenGeometry()
        # 获取调用对象的坐标数据
        size = self.geometry()
        # 移动作用于调用对象的中心位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def quit(self):
        self.close()

    def apply(self):
        if self.check_port(self.input.text()) != 5 or self.check_port(self.input2.text()) != 5:
            QMessageBox.warning(self, "提示", "端口号应为1025-65535之间的整数，请检查通信和计算端口号！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        if self.check_ip(self.input1.text()) != 0:
            QMessageBox.warning(self, "提示", "通信服务器IP格式不正确！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        for i in range(self.combo2.currentIndex() + 1):
            if self.check_ip(self.collect[1][i].text()) != 0:
                if i == 0:
                    temp = "计算服务器①IP格式不正确！"
                elif i == 1:
                    temp = "计算服务器②IP格式不正确！"
                elif i == 2:
                    temp = "计算服务器③IP格式不正确！"
                else:
                    temp = "出错了！"
                QMessageBox.warning(self, "提示", temp, QMessageBox.Yes,
                                    QMessageBox.Yes)
                return
        self.settings.setValue("port", self.input.text())
        self.settings.setValue("compute_port", self.input2.text())
        self.settings.setValue("communicate", self.input1.text())
        self.settings.setValue('computer_num', self.combo2.currentIndex() + 1)
        for i in range(3):
            if i <= self.combo2.currentIndex():
                self.settings.setValue("compute%d" % i, self.collect[1][i].text())
            else:
                self.settings.setValue('compute%d' % i, '')
        self.start.setEnabled(False)

    def check_port(self, s2):
        if len(s2) == 0:
            return 3
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

    def check_ip(self, s1):
        if len(s1) == 0:
            return 1
        for i in range(len(s1)):
            if s1[i] >= '0' and s1[i] <= '9' or s1[i] == '.':
                continue
            else:
                return 1
        s = s1.split('.')
        if len(s) != 4:
            return 1
        for l in s:
            if l == '':
                return 1
        for l in s:
            temp = int(l)
            if temp >= 0 and temp <= 255:
                continue
            else:
                return 2
        return 0


class Parameter(QWidget):
    def __init__(self, parent=None):
        super(Parameter, self).__init__(parent)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setFixedSize(600, 550)
        self.setWindowTitle("算法参数设置")
        self.settings = QSettings("configure", QSettings.IniFormat)
        self.display()
        self.center()

    def display(self):
        self.tips = QLabel(self)
        self.tips.setFont(QFont("楷体", 18))
        self.tips.setText("时间限制：")
        self.tips.setGeometry(50, 40, 160, 30)
        self.input = QSlider(Qt.Horizontal, self)
        self.input.setMinimum(1)
        self.input.setMaximum(40)
        self.input.setSingleStep(1)
        # self.input.setTickPosition(QSlider.TicksBelow)
        self.input.setGeometry(240, 40, 220, 30)
        self.input.setFont(QFont("楷体", 18))
        self.input.setValue(int(self.settings.value("time_limit", 10)))
        self.input.valueChanged.connect(self.setNum)
        self.num = QLabel(self)
        self.num.setFont(QFont("黑体", 15))
        self.num.setGeometry(470, 40, 50, 30)
        self.num.setText(str(self.settings.value("time_limit", 10)) + 's')

        self.tips1 = QLabel(self)
        self.tips1.setFont(QFont("楷体", 18))
        self.tips1.setText("进程数量：")
        self.tips1.setGeometry(50, 90, 160, 30)
        self.input1 = QComboBox(self)
        self.input1.setGeometry(240, 90, 100, 30)
        self.input1.setFont(QFont("宋体", 18))
        self.input1.addItems(
            ['  1  ', '  2  ', '  3  ', '  4  ', '  5  ', '  6  ', '  7  ', '  8  ', '  9  ', '  10  '])
        self.input1.setCurrentIndex(int(self.settings.value('process_num', 3)) - 1)
        # self.input1.setText(str(self.settings.value("node_num", "")))

        self.tips2 = QLabel(self)
        self.tips2.setFont(QFont("楷体", 18))
        self.tips2.setText("虚拟损失：")
        self.tips2.setGeometry(50, 140, 160, 30)
        self.input2 = QDial(self)
        self.input2.setGeometry(230, 130, 100, 50)
        self.input2.setFont(QFont("楷体", 18))
        self.input2.setMinimum(0)
        self.input2.setMaximum(20)
        self.input2.setSingleStep(2)
        self.input2.setValue(float(self.settings.value("virtual_loss", 20)) * 10)
        self.input2.valueChanged.connect(self.setNum1)
        self.num1 = QLabel(self)
        self.num1.setText(str(self.input2.value() / 10))
        self.num1.setGeometry(330, 140, 100, 30)
        self.num1.setFont(QFont("黑体", 10))

        self.tips3 = QLabel(self)
        self.tips3.setFont(QFont("楷体", 18))
        self.tips3.setText("UCB参数：")
        self.tips3.setGeometry(50, 190, 160, 30)
        self.input3 = QDoubleSpinBox(self)
        self.input3.setGeometry(240, 190, 100, 30)
        self.input3.setFont(QFont("楷体", 18))
        self.input3.setRange(0, 1.0)
        self.input3.setSingleStep(0.1)
        self.input3.setValue(float(self.settings.value("UCB_COEF", 1)))

        self.tips4 = QLabel(self)
        self.tips4.setFont(QFont("楷体", 18))
        self.tips4.setText("一次模拟局数：")
        self.tips4.setGeometry(50, 240, 160, 30)
        self.input4 = QComboBox(self)
        self.input4.setGeometry(240, 240, 100, 30)
        self.input4.setFont(QFont("楷体", 18))
        self.input4.addItems(['  1  ', '  2  ', '  3  ', '  4  ', '  5  '])
        self.input4.setCurrentIndex(int(self.settings.value("simulate_num", 1)) - 1)

        self.tips5 = QLabel(self)
        self.tips5.setFont(QFont("楷体", 18))
        self.tips5.setText("树结点总数：")
        self.tips5.setGeometry(50, 290, 160, 30)
        self.input5 = QLineEdit(self)
        self.input5.setGeometry(240, 290, 250, 30)
        self.input5.setFont(QFont("楷体", 18))
        self.input5.setText(str(self.settings.value("node_num", "")))

        self.tips6 = QLabel(self)
        self.tips6.setFont(QFont("楷体", 18))
        self.tips6.setText("最大扩展量：")
        self.tips6.setGeometry(50, 340, 160, 30)
        self.input6 = QLineEdit(self)
        self.input6.setGeometry(240, 340, 250, 30)
        self.input6.setFont(QFont("楷体", 18))
        self.input6.setText(str(self.settings.value("child_num", "")))

        self.tips7 = QLabel(self)
        self.tips7.setFont(QFont("楷体", 18))
        self.tips7.setText("最小访问数：")
        self.tips7.setGeometry(50, 390, 160, 30)
        self.input7 = QLineEdit(self)
        self.input7.setGeometry(240, 390, 250, 30)
        self.input7.setFont(QFont("楷体", 18))
        self.input7.setText(str(self.settings.value("min_visit_num", "")))

        self.tips8 = QLabel(self)
        self.tips8.setFont(QFont("楷体", 18))
        self.tips8.setText("最大访问数：")
        self.tips8.setGeometry(50, 440, 160, 30)
        self.input8 = QLineEdit(self)
        self.input8.setGeometry(240, 440, 250, 30)
        self.input8.setFont(QFont("楷体", 18))
        self.input8.setText(str(self.settings.value("max_visit_num", "")))

        self.start = QPushButton(self)
        self.start.setFont(QFont("黑体", 15))
        self.start.setText("应用")
        self.start.setGeometry(320, 500, 100, 30)
        self.start.clicked.connect(self.apply)

        self.stop = QPushButton(self)
        self.stop.setFont(QFont("黑体", 15))
        self.stop.setText("退出")
        self.stop.setGeometry(450, 500, 100, 30)
        self.stop.clicked.connect(self.quit)

    def setNum1(self):
        self.num1.setText(str(self.input2.value() / 10))

    def setNum(self):
        self.num.setText(str(self.input.value()) + 's')

    # 将窗口移至屏幕中心
    def center(self):
        # 获取屏幕坐标数据
        screen = QDesktopWidget().screenGeometry()
        # 获取调用对象的坐标数据
        size = self.geometry()
        # 移动作用于调用对象的中心位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def quit(self):
        self.close()

    def apply(self):
        if self.input5.text() == '' or self.input6.text() == '' or self.input7.text() == '' or self.input8.text() == '':
            QMessageBox.warning(self, "提示", "所有参数均不能为空！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        if int(self.input5.text()) < 2300 or int(self.input5.text()) > 500000:
            QMessageBox.warning(self, "提示", "树结点总数应在2300~500000之间！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        if int(self.input6.text()) < 2000 or int(self.input6.text()) > 2500:
            QMessageBox.warning(self, "提示", "最大扩展量应在2000~2500之间！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        if int(self.input7.text()) < 1 or int(self.input7.text()) > 50:
            QMessageBox.warning(self, "提示", "最小访问数应在1~50之间！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        if int(self.input8.text()) < 1 or int(self.input8.text()) > 1000000:
            QMessageBox.warning(self, "提示", "最大访问数应在0~1000000之间！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        if int(self.input7.text()) >= int(self.input8.text()):
            QMessageBox.warning(self, "提示", "最大访问数应比最小访问数大！", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        self.settings.setValue('time_limit', int(self.input.value()))
        self.settings.setValue('process_num', self.input1.currentIndex() + 1)
        self.settings.setValue('virtual_loss', self.input2.value() / 10)
        self.settings.setValue('UCB_COEF', float(self.input3.value()))
        self.settings.setValue('simulate_num', self.input4.currentIndex() + 1)
        self.settings.setValue('node_num', int(self.input5.text()))
        self.settings.setValue('child_num', int(self.input6.text()))
        self.settings.setValue('min_visit_num', int(self.input7.text()))
        self.settings.setValue('max_visit_num', int(self.input8.text()))
        self.start.setEnabled(False)


class Mode(QWidget):
    def __init__(self, parent=None):
        super(Mode, self).__init__(parent)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setFixedSize(500, 300)
        self.setWindowTitle("对战模式设置")
        self.settings = QSettings('configure', QSettings.IniFormat)
        self.display()

    def display(self):
        self.tips = QLabel(self)
        self.tips.setFont(QFont("微软雅黑", 18))
        self.tips.setGeometry(50, 48, 80, 30)
        self.tips.setText("正方:")
        self.input = QComboBox(self)
        self.input.setFont(QFont("黑体", 15))
        self.input.addItems(['Human', 'Computer'])
        self.input.setGeometry(150, 50, 200, 35)

        self.tips1 = QLabel(self)
        self.tips1.setFont(QFont("微软雅黑", 18))
        self.tips1.setGeometry(50, 138, 80, 30)
        self.tips1.setText("反方:")
        self.input1 = QComboBox(self)
        self.input1.setFont(QFont("黑体", 15))
        self.input1.addItems(['Human', 'Computer'])
        self.input1.setGeometry(150, 140, 200, 35)

        status = int(self.settings.value('status', 1))
        mode = int(self.settings.value('mode', 1))
        if mode == 1:
            self.input.setCurrentIndex(0)
            self.input1.setCurrentIndex(0)
        elif mode == 3:
            self.input.setCurrentIndex(1)
            self.input1.setCurrentIndex(1)
        else:
            if status == 1 or status == 4:
                self.input.setCurrentIndex(0)
                self.input1.setCurrentIndex(1)
            else:
                self.input.setCurrentIndex(1)
                self.input1.setCurrentIndex(0)

        self.input2 = QRadioButton(self)
        self.input2.setGeometry(380, 20, 100, 100)
        self.input2.setText("先手")
        self.input2.setFont(QFont("楷体", 10))

        self.input3 = QRadioButton(self)
        self.input3.setGeometry(380, 110, 100, 100)
        self.input3.setText("先手")
        self.input3.setFont(QFont("楷体", 10))

        flag = int(self.settings.value('status', 1))
        if flag == 1 or flag == 3:
            self.input2.setChecked(True)
        if flag == 2 or flag == 4:
            self.input3.setChecked(True)

        self.start = QPushButton(self)
        self.start.setFont(QFont("黑体", 15))
        self.start.setText("应用")
        self.start.setGeometry(250, 250, 100, 30)
        self.start.clicked.connect(self.apply)

        self.stop = QPushButton(self)
        self.stop.setFont(QFont("黑体", 15))
        self.stop.setText("退出")
        self.stop.setGeometry(380, 250, 100, 30)
        self.stop.clicked.connect(self.quit)

    def apply(self):
        plus = self.input.currentIndex()
        minus = self.input1.currentIndex()
        if self.input2.isChecked() == True:
            flag = 0
        else:
            flag = 1
        if plus == 0 and minus == 0:
            self.settings.setValue('status', flag + 1)
        elif plus == 0 and minus == 1:
            if flag == 0:
                self.settings.setValue('status', 1)
            else:
                self.settings.setValue('status', 4)
        elif plus == 1 and minus == 0:
            if flag == 0:
                self.settings.setValue('status', 3)
            else:
                self.settings.setValue('status', 2)
        else:
            self.settings.setValue('status', flag + 3)
        self.settings.setValue('mode', plus + minus + 1)
        self.start.setEnabled(False)

    def quit(self):
        self.close()


class Aspect(QWidget):
    def __init__(self, parent=None):
        super(Aspect, self).__init__(parent)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setFixedSize(800, 800)
        self.setWindowTitle("界面设置")
        self.settings = QSettings('configure', QSettings.IniFormat)
        self.display()

    def display(self):
        self.tip = QLabel(self)
        self.tip.setFont(QFont("楷体", 18))
        self.tip.setGeometry(40, 40, 60, 30)
        self.tip.setText("棋盘:")
        self.input = QComboBox(self)
        self.input.setFont(QFont("微软雅黑", 12))
        self.input.addItems(['    经  典    ', '    星  空    ', '    战  争    '])
        self.stock = ['chessboard.png', 'chessboard.png', 'chessboard.png']
        self.input.setCurrentIndex(self.stock.index(str(self.settings.value('chessboard', 'chessboard.png'))))
        self.input.setGeometry(140, 40, 200, 30)
        self.input.currentIndexChanged.connect(self.setIndex)

        self.show1 = QLabel(self)
        self.show1.setScaledContents(True)
        self.show1.setPixmap(QPixmap('./images/%s' % (self.stock[self.input.currentIndex()])))
        self.show1.setGeometry(430, 30, 200, 200)

        self.tip1 = QLabel(self)
        self.tip1.setFont(QFont("楷体", 18))
        self.tip1.setGeometry(40, 280, 60, 30)
        self.tip1.setText("正方:")
        self.input1 = QComboBox(self)
        self.input1.setFont(QFont("微软雅黑", 12))
        self.input1.addItems(['    经  典    ', '    星  空    ', '    战  争    '])
        self.stock1 = ['chess_white', 'chess_white', 'chess_white']
        self.input1.setCurrentIndex(self.stock1.index(str(self.settings.value('plus', 'chess_white'))))
        self.input1.setGeometry(140, 280, 200, 30)
        self.input1.currentIndexChanged.connect(self.setIndex1)

        self.show2 = QLabel(self)
        self.show2.setScaledContents(True)
        self.show2.setPixmap(QPixmap('./images/%s.png' % (self.stock1[self.input1.currentIndex()])))
        self.show2.setGeometry(180, 370, 100, 100)

        self.tip2 = QLabel(self)
        self.tip2.setFont(QFont("楷体", 18))
        self.tip2.setGeometry(440, 280, 60, 30)
        self.tip2.setText("反方:")
        self.input2 = QComboBox(self)
        self.input2.setFont(QFont("微软雅黑", 12))
        self.input2.addItems(['    经  典    ', '    星  空    ', '    战  争    '])
        self.stock2 = ['chess_black', 'chess_black', 'chess_black']
        self.input2.setCurrentIndex(self.stock2.index(str(self.settings.value('minus', 'chess_black'))))
        self.input2.setGeometry(520, 280, 200, 30)
        self.input2.currentIndexChanged.connect(self.setIndex2)

        self.show3 = QLabel(self)
        self.show3.setScaledContents(True)
        self.show3.setPixmap(QPixmap('./images/%s.png' % (self.stock2[self.input2.currentIndex()])))
        self.show3.setGeometry(560, 370, 100, 100)

        self.tip3 = QLabel(self)
        self.tip3.setFont(QFont("楷体", 18))
        self.tip3.setGeometry(40, 500, 60, 30)
        self.tip3.setText("粒子:")
        self.input3 = QComboBox(self)
        self.input3.setFont(QFont("微软雅黑", 12))
        self.input3.addItems(['    经  典    ', '    星  空    ', '    战  争    '])
        self.stock3 = ['ball', 'ball', 'ball']
        self.input3.setCurrentIndex(self.stock3.index(str(self.settings.value('ball', 'ball'))))
        self.input3.setGeometry(140, 500, 200, 30)
        self.input3.currentIndexChanged.connect(self.setIndex3)

        self.show4 = QLabel(self)
        self.show4.setScaledContents(True)
        self.show4.setPixmap(QPixmap('./images/%s.png' % (self.stock3[self.input3.currentIndex()])))
        self.show4.setGeometry(180, 590, 100, 100)

        self.tip4 = QLabel(self)
        self.tip4.setFont(QFont("楷体", 18))
        self.tip4.setGeometry(440, 500, 100, 30)
        self.tip4.setText("透明度:")
        self.tip5 = QLabel(self)
        self.tip5.setFont(QFont("楷体", 18))
        self.tip5.setGeometry(600, 500, 100, 30)
        self.tip5.setText("%d%%" % (int(float(self.settings.value('clarity', 1.0)) * 100)))
        self.input4 = QSlider(Qt.Horizontal, self)
        self.input4.setMinimum(0)
        self.input4.setMaximum(100)
        self.input4.setSingleStep(1)
        self.input4.setValue(int(float(self.settings.value('clarity', 1.0)) * 100))
        self.input4.setFont(QFont("微软雅黑", 15))
        self.input4.setGeometry(520, 530, 200, 30)
        self.input4.valueChanged.connect(self.setNum)

        self.start = QPushButton(self)
        self.start.setFont(QFont("黑体", 15))
        self.start.setText("应用")
        self.start.setGeometry(470, 740, 100, 30)
        self.start.clicked.connect(self.apply)

        self.stop = QPushButton(self)
        self.stop.setFont(QFont("黑体", 15))
        self.stop.setText("退出")
        self.stop.setGeometry(620, 740, 100, 30)
        self.stop.clicked.connect(self.quit)

    def setNum(self):
        self.tip5.setText('%d%%' % (self.input4.value()))

    def setIndex(self):
        self.show1.setPixmap(QPixmap('./images/%s' % (self.stock[self.input.currentIndex()])))

    def setIndex1(self):
        self.show2.setPixmap(QPixmap('./images/%s.png' % (self.stock1[self.input1.currentIndex()])))

    def setIndex2(self):
        self.show3.setPixmap(QPixmap('./images/%s.png' % (self.stock2[self.input2.currentIndex()])))

    def setIndex3(self):
        self.show3.setPixmap(QPixmap('./images/%s.png' % (self.stock2[self.input2.currentIndex()])))

    def apply(self):
        self.settings.setValue('chessboard', str(self.stock[self.input.currentIndex()]))
        self.settings.setValue('plus', str(self.stock1[self.input1.currentIndex()]))
        self.settings.setValue('minus', str(self.stock2[self.input2.currentIndex()]))
        self.settings.setValue('ball', str(self.stock3[self.input3.currentIndex()]))
        self.settings.setValue('clarity', self.input4.value() / 100)
        self.start.setEnabled(False)

    def quit(self):
        self.close()


class General(QTabWidget):
    def __init__(self):
        super(General, self).__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowTitle('设置')

        self.setTabShape(QTabWidget.Triangular)
        self.addTab(Parameter(), '参数设置')
        self.addTab(Function(), '功能分配')
        self.addTab(Mode(), '对战模式')
        self.addTab(Aspect(), '界面选择')
        self.setSize()

        self.currentChanged.connect(self.setSize)

    def setSize(self):
        if self.currentIndex() == 0:
            self.resize(600, 590)
        elif self.currentIndex() == 1:
            self.resize(600, 610)
        elif self.currentIndex() == 2:
            self.resize(500, 340)
        else:
            self.resize(800, 840)

class Situation(QScrollArea):
    def __init__(self,text='None'):
        super(Situation,self).__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowTitle('博弈实况')
        self.setFixedSize(400,500)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.test=QLabel()
        self.test.setFont(QFont('微软雅黑',20))
        self.test.setText(text)
        self.setWidget(self.test)
        self.ensureVisible(self.test.x()+self.test.width(),self.test.y()+self.test.height(),5,5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/moon_128px.ico"))
    # form = Parameter()
    # form = Function()
    # form = Mode()
    # form = Aspect()
    # form =General()
    text='---------博--弈--实--况---------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ndfs\n\n\n\n\nfgd'
    form=Situation(text)
    form.show()
    sys.exit(app.exec())
