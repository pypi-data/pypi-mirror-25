from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
form, base = uic.loadUiType("form.ui")
#from form import Ui_MainWindow
#form = Ui_MainWindow()


class MyWidget (QtWidgets.QMainWindow, form):
    def __init__(self, mixin_arg, **kwds):
        super().__init__(**kwds)
        self.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyWidget(None)
    form.show()
    app.exec_()
