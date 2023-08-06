from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo

cnx = pymongo.MongoClient()
db = cnx["selenium"]
tbl = db["customers"]

"""
class Spyder(object):
    driver = webdriver.Firefox()
    driver.get("http://paginasblancas.pe/")
    driver.find_element_by_xpath("//a[@data-target='address']").click()
    driver.find_element_by_name("street").send_keys("carlos izaguirre")
    driver.find_element_by_name("streetNumber").send_keys("2")
    driver.find_element_by_id("aLocality").send_keys(u"los olivos\ue007")
"""

source = ""
try:
    form, base = uic.loadUiType("BOT.ui")
    source = "ui"
except Exception as e:
    from form import Ui_MainWindow
    form = Ui_MainWindow
    source = "class"

class MyWidget (QtWidgets.QMainWindow, form):
    driverType = ""
    def __init__(self, mixin_arg, **kwds):
        super().__init__(**kwds)
        self.setupUi(self)
        self.__bind__()


    def __bind__(self):
        self.btnSend.clicked.connect(self.changeText)
        self.btnExit.clicked.connect(self.close)
        self.btnStart.clicked.connect(self.startBot)
        self.txtCommand.returnPressed.connect(self.txtCommand_keyPress)
        self.lsbxLog.currentItemChanged.connect(self.repeatCommand)

    def repeatCommand(self, current, previous):
        self.txtCommand.setText(current.text())
        print(current.text())
        #self.labelBigImageDisplay(current.pixmap())

    def changeText(self):
        global source
        self.lblDebug.setText(source + " - " + self.driverType + " - " +self.txtCommand.text())

    def txtCommand_keyPress(self):
        self.lsbxLog.addItem(self.txtCommand.text())
        self.txtCommand.clear()
        self.changeText()

    def startBot(self):
        if self.rbtnFirefox.isChecked():
            self.driverType = "Firefox"
        elif self.rbtnChrome.isChecked():
            self.driverType = "Chrome"
        else:
            self.driverType = "IE"


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyWidget(None)
    form.show()
    app.exec_()
