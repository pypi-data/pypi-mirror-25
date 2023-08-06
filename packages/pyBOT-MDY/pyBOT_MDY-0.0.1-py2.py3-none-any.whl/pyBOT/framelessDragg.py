from PyQt5.QtWidgets import (QMessageBox,QApplication, QWidget, QToolTip, QPushButton,
                             QDesktopWidget, QMainWindow, QAction, qApp, QToolBar, QVBoxLayout,
                             QComboBox,QLabel,QLineEdit,QGridLayout,QMenuBar,QMenu,QStatusBar,
                             QTextEdit,QDialog,QFrame,QProgressBar
                             )
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPalette
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer, QPoint

import sys
form, base = uic.loadUiType("pyBOT.ui")
class cssden(QMainWindow, form):

    def __init__(self, mixin_arg, **kwds):
        super().__init__(**kwds)
        self.setupUi(self)
    #def __init__(self):
        #super().__init__()


        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        #size
        self.setFixedSize(604,370)
        self.center()


        #label
        self.lbl = QLabel(self)
        self.lbl.setText("test")
        self.lbl.setStyleSheet("background-color: rgb(0,0,0);"
                               "border: 1px solid red;"
                               "color: rgb(255,255,255);"
                               "font: bold italic 20pt 'Times New Roman';")
        self.lbl.setGeometry(5,5,60,40)

        self.oldPos = self.pos()

        self.show()

    def alert(self):
        pass
    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

app = QApplication(sys.argv)
#app.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")

ex = cssden(None)
sys.exit(app.exec_())
