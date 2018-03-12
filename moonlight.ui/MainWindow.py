# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Interface(QMainWindow):
    #初始化主界面
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)
        self.resize(1100, 800)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(1100, 800)
        self.setWindowTitle("moonlight") 
        self.times=1
        self.menulayout()
        self.toollayout()
        self.GenerateBoard()
        self.center()
    
    #设置菜单栏
    def menulayout(self):
        self.bar=self.menuBar()
        #游戏的子菜单
        game=self.bar.addMenu(" 游  戏 ")
        newgame=QAction("新游戏", self)
        newgame.setShortcut("F5")
        game.addAction(newgame)
        pausegame=QAction("暂停游戏", self)
        pausegame.setShortcut("F6")
        game.addAction(pausegame)
        stopgame=QAction("停止游戏", self)
        stopgame.setShortcut("F7")
        game.addAction(stopgame)
        game.addSeparator()
        open=QAction("打开", self)
        open.setShortcut("Ctrl+O")
        game.addAction(open)
        save=QAction("保存", self)
        save.setShortcut("Ctrl+S")
        game.addAction(save)
        game.addSeparator()
        quit=QAction("退出", self)
        quit.setShortcut("Ctrl+Q")
        game.addAction(quit)
        #棋局控制的子菜单
        situation=self.bar.addMenu("棋局控制")
        up=QAction("后退一步", self)
        up.setShortcut("F9")
        situation.addAction(up)
        down=QAction("前进一步", self)
        down.setShortcut("F10")
        situation.addAction(down)
        up5=QAction("后退五步", self)
        up5.setShortcut("F11")
        situation.addAction(up5)
        down5=QAction("前进五步", self)
        down5.setShortcut("F12")
        situation.addAction(down5)
        start=QAction("回到开局", self)
        start.setShortcut("F1")
        situation.addAction(start)
        end=QAction("直达终局", self)
        end.setShortcut("F2")
        situation.addAction(end)
        #移动控制的子菜单
        movecontrol=self.bar.addMenu("移动控制")
        movenow=QAction("强制落子", self)
        movenow.setShortcut("Ctrl+R")
        movecontrol.addAction(movenow)
        suggest=QAction("走法建议", self)
        movecontrol.addAction(suggest)
        coordmove=QAction("坐标落子", self)
        movecontrol.addAction(coordmove)
        switchside=QAction("转换角色", self)
        movecontrol.addAction(switchside)
        #设置的子菜单
        setting=self.bar.addMenu(" 设  置 ")
        appearance=QAction("界面设置", self)
        setting.addAction(appearance)
        setting.addSeparator()
        gamemode=QAction("对战模式", self)
        setting.addAction(gamemode)
        parallelmode=QAction("并行模式", self)
        setting.addAction(parallelmode)
        setting.addSeparator()
        parameter=QAction("算法参数", self)
        parameter.setShortcut("Ctrl+H")
        setting.addAction(parameter)
        #视图的子菜单
        view=self.bar.addMenu(" 视  图 ")
        self.toolcolumn=QAction("工具栏", self)
        self.toolcolumn.setShortcut("Ctrl+T")
        #self.toolcolumn.setObjectName("toolcolumn")
        self.toolcolumn.setIcon(QIcon("./images/checked.png"))
        self.toolcolumn.triggered.connect(self.displaytoolbar)
        view.addAction(self.toolcolumn)
        textbox=QAction("文本框", self)
        view.addAction(textbox)
        movehistory=QAction("博弈实况", self)
        view.addAction(movehistory)
        #关于的子菜单
        about=self.bar.addMenu(" 帮  助 ")
        copyinfo=QAction("关于moonlight", self)
        copyinfo.setShortcut("Ctrl+I")
        about.addAction(copyinfo)
        help=QAction("技术相关", self)
        about.addAction(help)
    
    #设置工具栏
    def toollayout(self):
        self.tb=QToolBar()
        self.tb.setObjectName("tb")
        start=QAction(QIcon("./images/Start.png"), "开始&继续", self)
        self.tb.addAction(start)
        pause=QAction(QIcon("./images/Pause.png"), "暂停", self)
        self.tb.addAction(pause)
        stop=QAction(QIcon("./images/Stop_red.png"), "停止", self)
        self.tb.addAction(stop)
        self.tb.addSeparator()
        open=QAction(QIcon("./images/open_file.png"), "打开", self)
        self.tb.addAction(open)
        save=QAction(QIcon("./images/Save.png"), "保存", self)
        self.tb.addAction(save)
        self.tb.addSeparator()
        Hide_left_left=QAction(QIcon("./images/Hide_left_left.png"), "回到开局", self)
        self.tb.addAction(Hide_left_left)
        Hide_left=QAction(QIcon("./images/Hide_left.png"), "后退五步", self)
        self.tb.addAction(Hide_left)
        left=QAction(QIcon("./images/left.png"), "后退一步", self)
        self.tb.addAction(left)
        right=QAction(QIcon("./images/right.png"), "前进一步", self)
        self.tb.addAction(right)
        Hide_right=QAction(QIcon("./images/Hide_right.png"), "前进五步", self)
        self.tb.addAction(Hide_right)
        Hide_right_right=QAction(QIcon("./images/Hide_right_right.png"), "直达终局", self)
        self.tb.addAction(Hide_right_right)
        self.tb.addSeparator()
        Prohibit=QAction(QIcon("./images/Prohibit.png"), "强制落子", self)
        self.tb.addAction(Prohibit)
        Analyze=QAction(QIcon("./images/Analyze.png"), "分析", self)
        self.tb.addAction(Analyze)
        Suggest=QAction(QIcon("./images/Suggest.png"), "建议", self)
        self.tb.addAction(Suggest)
        self.tb.addSeparator()
        Situation=QAction(QIcon("./images/Situation.png"), "博弈实况", self)
        self.tb.addAction(Situation)
        Info=QAction(QIcon("./images/Info.png"), "文本窗口", self)
        self.tb.addAction(Info)
        Setting=QAction(QIcon("./images/Setting.png"), "设置", self)
        self.tb.addAction(Setting)
        self.tb.addSeparator()
        Sound=QAction(QIcon("./images/Sound.png"), "声音", self)
        self.tb.addAction(Sound)
        self.addToolBar(self.tb)
        
    #将窗口移至屏幕中心
    def center(self):
        #获取屏幕坐标数据
        screen=QDesktopWidget().screenGeometry()
        #获取调用对象的坐标数据
        size=self.geometry()
        #移动作用于调用对象的中心位置
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)    
    
    #显示工具栏
    def displaytoolbar(self):
        if self.times==0:
            self.times=1
            self.toolcolumn.setIcon(QIcon("./images/checked.png"))
            self.tb.setVisible(True)
        else:
            self.times=0
            self.toolcolumn.setIcon(QIcon())
            self.tb.setVisible(False)
    #显示棋盘
    def GenerateBoard(self):
        
        self.centralwidget=QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.chess=QLabel(self.centralwidget)
        minsize=min(self.centralwidget.width()/3*2-40, self.centralwidget.height()-20)
        self.chess.setGeometry(20, 20, minsize, minsize)
        '''self.chess.setPixmap(QPixmap.fromImage(QImage("./images/chessboard.png").\
                scaled(1000, 1000, Qt.KeepAspectRatio).\
                scaled(self.gridlayoutwidget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        '''
        self.chess.setPixmap(QPixmap("./images/chessboard.png"))
        self.chess.setScaledContents(True)
        self.display=QLabel(self.centralwidget)
        self.display.setFont(QFont("微软雅黑", 12))
        self.display.setAlignment(Qt.AlignTop)
        self.text="玩家————————————————————————————————————————————————————————\n\n    白方：    \n    黑方：    \n\n\n\
游戏时间——————————————————————————————————————————————————————\n\n    白方：    \n    黑方：    \n\n\n当前行为\
——————————————————————————————————————————————————————————\n\n    None\n\n\n状态\
————————————————————————————————————————————————————————\n\n    游戏状态：    \n    估值：    \n    走法总数：    "
        self.display.setText(self.text)
        self.display.setGeometry(self.centralwidget.width()/3*2, 20, self.centralwidget.width()/3-40, self.centralwidget.height()-40)
        
    #窗口大小改变事件
    def resizeEvent(self, event):
        minsize=min(self.centralwidget.width()/3*2-40, self.centralwidget.height()-40)
        self.chess.setGeometry(20, 20, minsize, minsize)
        self.display.setGeometry(self.centralwidget.width()/3*2, 20, self.centralwidget.width()/3-40, self.centralwidget.height()-40)

if __name__=="__main__":
    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/moon_128px.ico"))
    form=Interface()
    form.show()
    sys.exit(app.exec())
